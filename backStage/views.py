# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from forms import AddApiForm,AddProject,AddScene,AddGooflow
from models import SingleApi,ProjectInfo,sceneInfo,ReferData,runLog,FlowSheet
from tasks import runApi,runScene,countTime
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from generateDict import gDict,getApiData,SqlDML,getAllDate
import json
from collections import OrderedDict
# Create your views here.

#--------------------404页面

def page_not_found(request):
	return render(request,"404.html")


#--------------------500页面

def page_error(request):
	return render(request,"500.html")

#--------------------首页
def index(request):
	return render(request,"index.html")

#--------------------欢迎页
def welcome(request):
	if request.method == 'GET':
		context={'api':['dd','cc','ee'],'apicount':[1,2,3],'faild':[1,2,3],
				'success':[1,2,3]}
		return render(request,"welcome.html",{'context':context})



#--------------------接口列表页
def memberlist(request):
	if request.method == 'GET':
		api = SingleApi.objects.all()
		print api
		project = ProjectInfo.objects.all()
	context={"apilist":api,"project":project}
	return render(request,"member-list.html",context)

#--------------------新增接口页面
def memberadd(request):
	if request.method == 'GET':
		project = ProjectInfo.objects.all()
		context = {"project":project}
		return render(request,"member-add.html",context)

def membershow(request):
	return render(request,"member-show.html")

#--------------------查询接口
def searchApi(request,ProId):
	if request.method == 'GET':
		try:
			api = SingleApi.objects.filter(projectName=ProId).values()
			proModel = ProjectInfo.objects.filter(pk=ProId).first()
			proName = proModel.ProjectName
			#u_dict = model_to_dict(api)
		except ObjectDoesNotExist as e:
			print e
			api = {}
		#import json
		dict1 = gDict(api)
		# c = json.dumps(dict1)
		for k,v in dict1.items():
			v['projectName_id'] = proName
		print dict1
		return JsonResponse({'apilist':dict1})

#--------------------编辑接口
def editApi(request,ApiId):
	if request.method == 'GET':
		api = SingleApi.objects.filter(pk=ApiId).first()
		project = ProjectInfo.objects.all()
		project_id = api.projectName.id
		context={"apiData":api,"project":project,"projectId":project_id}		
		return render(request,"member-edit.html",context)
	else:
		addApiForm = AddApiForm(request.POST)
		if addApiForm.is_valid():
			APIName = addApiForm.cleaned_data.get('APIName',None)
			requestMethod = addApiForm.cleaned_data.get('requestMethod',None)
			requestHeaderData = addApiForm.cleaned_data.get('requestHeaderData',None)
			requestSubmitMethod = addApiForm.cleaned_data.get('requestSubmitMethod',None)
			APIAddress = addApiForm.cleaned_data.get('APIAddress',None)
			requestData = addApiForm.cleaned_data.get('requestData',None)
			ProjectId = addApiForm.cleaned_data.get('ProjectId',None)
			project = ProjectInfo.objects.filter(pk=ProjectId).first()
			SingleApi.objects.select_for_update().filter(pk=ApiId).update(APIName=APIName,
			requestMethod=requestMethod,
			requestHeaderData=requestHeaderData,
			requestSubmitMethod=requestSubmitMethod,
			APIAddress=APIAddress,
			requestData=requestData,
			projectName=project,)
			
			print 'save successful'
			return JsonResponse({"code":200})
		else:
			return JsonResponse({"errors":addApiForm.errors})

#--------------------新增接口
def addApi(request):
	if request.method == 'GET':
		return HttpResponse(u"请求方式错误")
	else:
		addApiForm = AddApiForm(request.POST)
		if addApiForm.is_valid():
			APIName = addApiForm.cleaned_data.get('APIName',None)
			requestMethod = addApiForm.cleaned_data.get('requestMethod',None)
			requestHeaderData = addApiForm.cleaned_data.get('requestHeaderData',None)
			requestSubmitMethod = addApiForm.cleaned_data.get('requestSubmitMethod',None)
			APIAddress = addApiForm.cleaned_data.get('APIAddress',None)
			requestData = addApiForm.cleaned_data.get('requestData',None)
			ProjectId = addApiForm.cleaned_data.get('ProjectId',None)
			project = ProjectInfo.objects.filter(pk=ProjectId).first()
			singleApi = SingleApi(APIName=APIName,
								  requestMethod=requestMethod,
								  requestHeaderData= requestHeaderData,
								  requestSubmitMethod=requestSubmitMethod,
								  APIAddress=APIAddress,
								  requestData=requestData,
								  projectName=project,)
			singleApi.save()
			return JsonResponse({"code":"200"})
		else:
			return JsonResponse({"error":addApiForm.errors})

#--------------------删除接口
def delApi(request,ApiId):
	if request.method == 'GET':
		return HttpResponse(u"请求方式错误")
	else:
		api = SingleApi.objects.filter(pk=ApiId)
		if api:
			api.delete()
			return JsonResponse({"code":"200"})
		else:
			return JsonResponse({"errors":u"未知错误"})

#--------------------产品列表界面
def listProject(request):
	if request.method == 'GET':
		project = ProjectInfo.objects.all()
		context={"project":project}
		return render(request,"admin-permission.html",context)


#--------------------新增产品
def addProject(request):
	if request.method == 'GET':
		return render(request,"add-project.html")
	else:
		projectForm = AddProject(request.POST)
		if projectForm.is_valid():
			projectName = projectForm.cleaned_data.get('ProjectName',None)
			projectDes = projectForm.cleaned_data.get('ProjectDes',None)
			projectInfo = ProjectInfo(ProjectName=projectName,
									  ProjectDes=projectDes,)
			projectInfo.save()
			return JsonResponse({"code":"200"})
		else:
			return JsonResponse({"error":projectForm.errors})
#-------------------编辑产品
def editProject(request,PID):
	if request.method == 'GET':
		ProObject = ProjectInfo.objects.filter(pk=PID).first()
		context = {'projectName':ProObject.ProjectName,'projectDesc':ProObject.ProjectDes,'projectId':PID}
		return render(request,"edit-project.html",context)
	if request.method == 'POST':
		projectForm = AddProject(request.POST)
		if projectForm.is_valid():
			projectName = projectForm.cleaned_data.get('ProjectName',None)
			projectDes = projectForm.cleaned_data.get('ProjectDes',None)
			ProjectInfo.objects.select_for_update().filter(pk=PID).update(ProjectName=projectName,
																		  ProjectDes=projectDes)
			return JsonResponse({"code":"200"})
		else:
			return JsonResponse({"error":projectForm.errors})
#-------------------删除产品
def delProject(request,ProId):
	if request.method == 'GET':
		return HttpResponse(u'请求方式有问题')
	else:
		pro = ProjectInfo.objects.filter(pk=ProId).first()
		if pro:
			pro.delete()
			return JsonResponse({"code":"200"})
		else:
			return JsonResponse({"errors":u"未知错误"})


def callbackApi(func):
	result = func.status

def flowList(request):
	if request.method == 'GET':
		flowObject = FlowSheet.objects.all()
		context = {'flow':flowObject}
		return render(request,'picture-list.html',context)

#--------------------新增流程图
def addGooflow(request):
	if request.method == 'GET':
		projectObject = ProjectInfo.objects.all()
		context={'projectObject':projectObject}
		return render(request,'gooflow.html',context)
	if request.method == 'POST':
		flowObject = AddGooflow(request.POST)
		if flowObject.is_valid():
			FlowName = flowObject.cleaned_data.get("FlowName",None)
			FlowDes = flowObject.cleaned_data.get("FlowDes",None)
			rawData = flowObject.cleaned_data.get("rawData",None)
			projectName = flowObject.cleaned_data.get("projectName",None)
			project = ProjectInfo.objects.filter(pk=projectName).first()
			executeIdlist = []
			for sceneId in json.loads(rawData)['nodes'].items():
				executeIdlist.append(sceneId[1]['SceneID'])
			print executeIdlist
			executeId = ','.join(executeIdlist)
			flowModel = FlowSheet(FlowName=FlowName,
								  FlowDes=FlowDes,
								  rawData=rawData,
								  projectName=project,
								  executeId=executeId,
								  status='4')
			flowModel.save()
			return JsonResponse({"code":"200"})
		return JsonResponse({"errors":flowObject.errors})


def getSceneId(request):
	if request.method == 'GET':
		SceneIdDict = sceneInfo.objects.all().values()
		SceneIdList = gDict(SceneIdDict)
		return JsonResponse(SceneIdList)

#--------------------场景列表
def manageScene(request):
	if request.method == 'GET':
		project = ProjectInfo.objects.all()
		sceneinfo = sceneInfo.objects.all()
		context={"project":project,'sceneinfo':sceneinfo}

		return render(request,'manageScene.html',context)

#--------------------预览场景
def viewScene(request,SceneId):
	if request.method == 'GET':
		scenename = sceneInfo.objects.filter(pk=SceneId).first()
		idList = scenename.sceneIdList
		resultId = idList.split(',')[0:-1]
		api = SingleApi.objects.filter(pk__in=resultId).values()
		context = {'scenename':scenename,'api':api}
		return render(request,'member-show.html',context)
	elif request.method == 'POST':
		pass
		


#--------------------制造场景
def makeScene(request,ProId):
	if request.method == 'GET':
		project = ProjectInfo.objects.all()
		api = SingleApi.objects.all()
		sceneinfo = sceneInfo.objects.filter(projectName=ProId).values()
		context={"project":project,"api":api,"sceneinfo":sceneinfo,'proId':int(ProId)}
		return render(request,'makeScene.html',context)
	else:
		sceneForm = AddScene(request.POST)
		if sceneForm.is_valid():
			scenename = sceneForm.cleaned_data.get('sceneName',None)
			apilist = request.POST.getlist('apiList[]',None)
			projectname = sceneForm.cleaned_data.get('projectName',None)
			apiId = ''
			for api in apilist:
				apiId+=str(api)+','
			project = ProjectInfo.objects.filter(pk=projectname).first()
			sceneinfo = sceneInfo(sceneName=scenename,sceneIdList=apiId,projectName=project)
			sceneinfo.save()
			print '-------------------------','scenename',scenename,'apilist',apiId,'projectname',projectname
			sceneinfo = sceneInfo.objects.filter(projectName=projectname).values()
			print sceneinfo
			# jsonResult = gDict(sceneinfo)
			return JsonResponse({'code':0})
		else:
			return JsonResponse({"error":sceneForm.errors})



#--------------------查询场景
def searchScene(request,projectId):
	if request.method == 'GET':
		apiModel = SingleApi.objects.filter(projectName=projectId).values()
		dict2 = gDict(apiModel)
		return JsonResponse({'apilist':dict2})

#--------------------测试接口
def testApi(request,ApiId):
	#[0]url [1]header [2]data [3]method [4]submit 
		if request.method == 'GET':
			testData = getApiData(ApiId)
		data = testData[2]
		if testData[2]:
			data = json.loads(testData[2])
		try:
			run=runApi.delay(url=testData[0],
							headers=testData[1],
							data=data,
							method=testData[3],
							submit=testData[4])
			# result = run.result()
			result = run.get(timeout=6)
			#Eresult = run.get(propagate=False)
			#Eresult = run.wait()

		except Exception as e:
			print e
			return HttpResponse(e)
		# try:
		SingleApi.objects.select_for_update().filter(pk=ApiId).update(testResult=result.text,testHeader=json.dumps(dict(result.headers)))
		# except 
		if result.status_code == 200:
			SingleApi.objects.select_for_update().filter(pk=ApiId).update(failedOrTrue=True)
		else:
			SingleApi.objects.select_for_update().filter(pk=ApiId).update(failedOrTrue=False)
		context = {'requestData':testData[2],'result':result.text}
		return render(request,'testResult.html',context)

def testScene(request,SceneId):
	if request.method == 'GET':
		apiId = sceneInfo.objects.filter(pk=SceneId).first()
		apiIdList = apiId.sceneIdList.split(',')[:-1]
		referD = {}
		for ID in apiIdList:
			APIID = ReferData.objects.filter(apiName=ID).first()
			APIDATA = getApiData(ID)
			referD[ID] = {'ResultData':[],'HeaderData':[],'relyapi':APIID.relyApi,'apiData':APIDATA}
		for k,v in referD.items():
			referHeaderObject = ReferData.objects.filter(apiName=k).values()
			referHeaderDict = gDict(referHeaderObject)
			for kr,vr in referHeaderDict.items():
				if vr['referResultData']:
					referD[k]['ResultData'].append(vr['referResultData'])
				elif vr['referHeaderData']:
					referD[k]['HeaderData'].append(vr['referHeaderData'])
		# for key in sorted(referD.items()):

		for k,v in referD.items():
			try:
				run=runScene.delay(url=v['apiData'][0],
								headers=v['apiData'][1],
								data=v['apiData'][2],
								method=v['apiData'][3],
								submit=v['apiData'][4],
								APIID=v['apiData'][5],
								rely=v['relyapi'],
								headerList=v['HeaderData'],
								resultList=v['ResultData'],
								)
				# result = run.result()
				result = run.get(timeout=6)
				#Eresult = run.get(propagate=False)
				#Eresult = run.wait()

			except Exception as e:
				print e
				return HttpResponse(e)

		return JsonResponse({"message":"请求完成"})

#--------------------添加引用数据

def viewDataLog(request):
	if request.method == 'GET':
		JsonObject = {}
		SelectAllDate = runLog.objects.raw(getAllDate())
		for i in SelectAllDate:
			JsonObject[i.runDate] = [0,0]
		SelectFailedResult = runLog.objects.raw(SqlDML(0))
		for i in SelectFailedResult:
			if isinstance(i.failedOrTrue,bool):
				JsonObject[i.runDate] = [0,1]
			else:
				JsonObject[i.runDate] = [0,i.failedOrTrue]
		SelectOkResult = runLog.objects.raw(SqlDML(1))

		for i in SelectOkResult:
			if isinstance(i.failedOrTrue,bool):
				JsonObject[i.runDate][0] = 1
			else:
				JsonObject[i.runDate][0]= i.failedOrTrue
		print JsonObject
		return HttpResponse(json.dumps(OrderedDict(sorted(JsonObject.items()))), content_type="application/json")  
		
def addReferData(request,ApiId):
	if request.method == "GET":
		refer = ReferData.objects.filter(apiName=ApiId).values()
		referDict = gDict(refer)
		return JsonResponse(referDict)
	if request.method == "POST":
		jsonResult = eval(request.POST.get('datas',None))
		#使用创建方法
		relyapi = jsonResult['relyapi']
		apiInstance = SingleApi.objects.filter(pk=ApiId).first()
		createData = jsonResult.get('createData',None)
		updateData = jsonResult.get('updateData',None)
		for ck,cv in createData.items():
			if 'left' in ck:
				referModel = ReferData(referHeaderData=cv,apiName=apiInstance,relyApi=relyapi)
				referModel.save()
			if 'right' in ck:
				referModel = ReferData(referResultData=cv,apiName=apiInstance,relyApi=relyapi)
				referModel.save()
		for uk,uv in updateData.items():
			if 'left' in uk:
				indexId = uk[uk.find('t')+1:]
				print relyapi
				ReferData.objects.select_for_update().filter(pk=indexId).update(referHeaderData=uv,relyApi=relyapi)
			if 'right' in uk:
				indexId = uk[uk.find('t')+1:]
				print relyapi
				ReferData.objects.select_for_update().filter(pk=indexId).update(referResultData=uv,relyApi=relyapi)
		return JsonResponse({"code":"200"})
	else:
		return JsonResponse({"code":u"未知错误"})



# import requests
# import re
# import sysreload(sys)
# sys.setdefaultencoding('utf-8')
# type = sys.getfilesystemencoding()
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}
# html.encoding = 'utf-8'# gb18030TypeStr = unicodeTypeStr.encode("GB18030");


