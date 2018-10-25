#coding:utf-8
from celery import task,Celery
import requests
import json
from models import SingleApi,runLog
from datetime import datetime
@task
def runApi(url,headers,data,method,submit):
	headers = json.loads(headers)
	if method == 1 and submit == 1:
		json_request = requests.get(url=url,headers=headers,data=json.dumps(data))
	elif method == 1 and submit == 2:
		print "function at here,_________",type(data)
		json_request = requests.get(url=url,headers=headers,params=data)
	elif method == 2 and submit == 1:
		json_request = requests.post(url=url,headers=headers,data=json.dumps(data))
	elif method == 2 and submit == 2:
		print "zheli_______________________"
		json_request = requests.post(url=url,headers=headers,params=data)
	print "request success__________________________________________"
	return json_request


@task
def runScene(url,headers,data,method,submit,APIID,rely,headerList=None,resultList=None):

	print url,headers,data,method,submit,headerList,resultList,rely
	if headerList or resultList:
		try:
			headers = json.loads(headers)	
			results = json.loads(data)	
		except ValueError as e:
			headers = {}
			results = {}
		AData = SingleApi.objects.filter(pk=rely).first()
		print "__________________________test json.loads",type(AData.testHeader)
		try:
			headerDataSource = json.loads(AData.testHeader)
			resultDataSource = json.loads(AData.testResult)
		except ValueError as e:
			headerDataSource = {}
			resultDataSource = {}
		for header in headerList:
			if header in headerDataSource:
				headers.update({header:headerDataSource[header]})
		for result in resultList:
			if result in resultDataSource:
				results.update({result:resultDataSource[result]})
		if method == 1 and submit == 1:
			json_request = requests.get(url=url,headers=headers,data=json.dumps(results))
		elif method == 1 and submit == 2:
			json_request = requests.get(url=url,headers=headers,params=json.dumps(results))
		elif method == 2 and submit == 1:
			json_request = requests.post(url=url,headers=headers,data=json.dumps(results))
		elif method == 2 and submit == 2:
			print "zheli_______________________"
			json_request = requests.post(url=url,headers=headers,params=results)
		print "request success__________________________________________"
		SingleApi.objects.select_for_update().filter(pk=APIID).update(testResult=json_request.text,testHeader=json.dumps(dict(json_request.headers)))
		# except 
		ForeignKApi = SingleApi.objects.filter(pk=APIID).first()
		if json_request.status_code == 200:
			SingleApi.objects.select_for_update().filter(pk=APIID).update(failedOrTrue=True)
			print datetime.now()
			logObject = runLog(apiName=ForeignKApi,failedOrTrue=True,runDate=datetime.now()+datetime.timedelta(hours=8))
			print "接口运行成功正在记录日志"
			logObject.save()
		else:
			SingleApi.objects.select_for_update().filter(pk=APIID).update(failedOrTrue=False)
			print datetime.now()
			logObject = runLog(apiName=ForeignKApi,failedOrTrue=False,runDate=datetime.now()+datetime.timedelta(hours=8))
			print "接口运行失败正在记录日志"
			logObject.save()
	return json_request

@task
def countTime():
	import time
	time.sleep(20)
	print time.time()
