# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

# Create your models here.
class SingleApi(models.Model):
	APIName = models.CharField(blank=False,max_length=500)
	requestMethod = models.IntegerField(blank=False)
	requestHeaderData = models.CharField(blank=True,max_length=500)
	requestSubmitMethod = models.IntegerField(blank=False)
	APIAddress = models.CharField(blank=False,max_length=500)
	requestData = models.CharField(max_length=500)
	createtime = models.DateField(auto_now_add=True)
	file = models.CharField(max_length=100)
	projectName = models.ForeignKey('ProjectInfo')
	testResult = models.TextField()
	testHeader = models.TextField()
	failedOrTrue = models.BooleanField(blank=True)
	

class sceneInfo(models.Model):
	projectName = models.ForeignKey('ProjectInfo')
	sceneName = models.CharField(max_length=31)
	sceneIdList = models.CharField(max_length=100)
	createtime = models.DateField(auto_now_add=True)

class ProjectInfo(models.Model):
	ProjectName = models.CharField(blank=True,max_length=32)
	ProjectDes = models.CharField(null=True,max_length=500)

class ReferData(models.Model):
	apiName = models.ForeignKey('SingleApi')
	relyApi = models.CharField(blank=False,max_length=20)
	referResultData = models.CharField(blank=False,max_length=500)
	referHeaderData = models.CharField(blank=False,max_length=500)

class runLog(models.Model):
	apiName = models.ForeignKey('SingleApi')
	runDate = models.DateTimeField()
	failedOrTrue = models.BooleanField(blank=False)


class FlowSheet(models.Model):
	RUN_STATUS = (
		(u'1', u'NOTSTART'),
		(u'2', u'BEGINNING'),
		(u'3', u'ENDED')
	)
	FlowName = models.CharField(blank=False,max_length=50)
	FlowDes = models.CharField(blank=True,max_length=500)
	projectName = models.ForeignKey('ProjectInfo')
	createtime = models.DateField(auto_now_add=True)
	status = models.CharField(max_length=20,choices=RUN_STATUS)
	rawData = models.TextField()
	executeId = models.CharField(max_length=100)







