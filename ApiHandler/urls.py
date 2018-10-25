"""ApiHandler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from backStage import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404,handler500
#(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_URL}),


handler404 = "backStage.views.page_not_found"
handler500 = "backStage.views.page_error"


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$',views.index),
    url(r'^welcome/',views.welcome,name='welcome'),
    url(r'^memberlist/',views.memberlist,name='apilist'),
    url(r'^memberadd/',views.memberadd,name='add'),
    url(r'^membershow/',views.membershow,name='show'),
    url(r'^addApi/',views.addApi,name='addApi'),
    url(r'^delApi/(?P<ApiId>\d+)',views.delApi,name='delApi'),
    url(r'^editApi/(?P<ApiId>\d+)',views.editApi,name='editApi'),
    url(r'^runApi/$',views.testApi,name='runApi'),
    url(r'^listProject/',views.listProject,name='listProject'),
    url(r'^addProject/',views.addProject,name='addProject'),
    url(r'^editProject/(?P<PID>\d+)',views.editProject,name='editProject'),
    url(r'^testApi/(?P<ApiId>\d+)',views.testApi,name='testApi'),
    url(r'^flowList/',views.flowList,name='flowList'),
    url(r'^addGooflow/$',views.addGooflow,name='addGooflow'),
    url(r'^manageScene/',views.manageScene,name='manageScene'),
    url(r'^makeScene/(?P<ProId>\d+)',views.makeScene,name='makeScene'),
    url(r'^searchApi/(?P<ProId>\d+)',views.searchApi,name='searchApi'),
    url(r'^searchScene/(?P<projectId>\d+)',views.searchScene,name='searchScene'),
    url(r'^viewScene/(?P<SceneId>\d+)',views.viewScene,name='viewScene'),
    url(r'^delProject/(?P<ProId>\d+)',views.delProject,name='delProject'),
    url(r'^testScene/(?P<SceneId>\d+)',views.testScene,name='testScene'),
    url(r'^addReferData/(?P<ApiId>\d+)',views.addReferData,name='addReferData'),
    url(r'^getSceneId/',views.getSceneId,name='getSceneId'),
    url(r'^viewDataLog/',views.viewDataLog,name='viewDataLog'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
