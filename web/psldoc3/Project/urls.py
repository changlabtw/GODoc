"""Project URL Configuration

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
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from Protein.views import history,load_file,search_post,result,upload_file,download_file,goto_searchpost
from django.views.decorators.cache import cache_page
from django.views.static import serve
urlpatterns = [
    url(r'^admin/',(admin.site.urls)),
    url(r'^psldoc3$', (search_post)),
    url(r'^history$',(history)),
    url(r'^result$',(result)),
    url(r'^goto_searchpost$',(goto_searchpost)),
    url(r'^result/download_file$',download_file),
    url(r'^history/upload_file$',(upload_file)),
    url(r'^history/download_file$',download_file),
    url(r'^loading$',load_file),
    url(r'^static/([a-z]+.[a-z]+)',serve,{'document_root':'./images'}),  
 # url(r'^', include('course.urls', namespace='course')),
]
