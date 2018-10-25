#coding:utf-8
from models import SingleApi,ProjectInfo,sceneInfo,ReferData
def gDict(model):
	dict2 = {}
	for i in range(len(model)):
		dict2['A'+str(i)] = model[i]
	return dict2

def getApiData(ApiId):
	apiData = SingleApi.objects.filter(pk=ApiId).first()
	url = apiData.APIAddress
	headers = apiData.requestHeaderData
	data = apiData.requestData
	method = apiData.requestMethod
	submit = apiData.requestSubmitMethod
	return [url,headers,data,method,submit,ApiId]

def testAPI():
	pass


def SqlDML(target):
	query = """SELECT id,COUNT(failedOrTrue) as failedOrTrue,runDate FROM 
					(SELECT Id,failedOrTrue,apiname_id,DATE_FORMAT(rundate,"%%Y-%%m-%%d") AS runDate,MAX(rundate) AS MaxDate
					FROM backstage_runlog 
					GROUP BY apiname_id,DATE_FORMAT(rundate,'%%Y-%%m-%%d')) b WHERE failedOrTrue = """+str(target)+""" GROUP BY runDate""" 
	return query

def getAllDate():
	query = """SELECT id,failedOrTrue,apiname_id,DATE_FORMAT(rundate,"%%Y-%%m-%%d") AS runDate,MAX(rundate) AS MaxDate
					FROM backstage_runlog 
					GROUP BY apiname_id,DATE_FORMAT(rundate,'%%Y-%%m-%%d')"""
	return query



