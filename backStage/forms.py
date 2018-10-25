#coding:utf-8
from django import forms

class AddApiForm(forms.Form):
	APIName = forms.CharField(required=True)
	requestMethod = forms.IntegerField(required=True)
	requestHeaderData = forms.CharField(required=True)
	requestSubmitMethod = forms.IntegerField(required=True)
	APIAddress = forms.CharField(required=True)
	requestData = forms.CharField(required=False)
	ProjectId = forms.IntegerField(required=True)

	def clean_APIName(self):
		APIName = self.cleaned_data.get('APIName',None)
		if not APIName:
			raise forms.ValidationError(u'API名称不能为空',code = 'min_length')
		return APIName

	def clean_requestMethod(self):
		requestMethod = self.cleaned_data.get('requestMethod',None)
		if not requestMethod:
			raise forms.ValidationError(u'请求方式不能为空',code = 'min_length')
		return requestMethod

	def clean_requestHeaderData(self):
		requestHeaderData = self.cleaned_data.get('requestHeaderData',None)
		if not requestHeaderData:
			raise forms.ValidationError(u'请求header不能为空',code = 'min_length')
		return requestHeaderData

	def clean_requestSubmitMethod(self):
		requestSubmitMethod = self.cleaned_data.get('requestSubmitMethod',None)
		if not requestSubmitMethod:
			raise forms.ValidationError(u'请求提交方式不能为空',code = 'min_length')
		return requestSubmitMethod

	def clean_APIAddress(self):
		APIAddress = self.cleaned_data.get('APIAddress',None)
		if not APIAddress:
			raise forms.ValidationError(u'接口地址不能为空',code = 'min_length')
		return APIAddress

class AddProject(forms.Form):
	ProjectName = forms.CharField(required=True)
	ProjectDes = forms.CharField(required=False)



class AddScene(forms.Form):
	sceneName = forms.CharField(required=True)
	apiList = forms.CharField(required=False)
	projectName = forms.CharField(required=True)

class AddGooflow(forms.Form):

	FlowName = forms.CharField(required=False)
	FlowDes = forms.CharField(required=False)
	status = forms.BooleanField(required=False)
	rawData = forms.CharField()
	projectName = forms.CharField(required=False)