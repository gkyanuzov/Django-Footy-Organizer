"""SofiaFooty URL Configuration

The `urlpatterns` list routes URLs to views_p. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views_p
    1. Add an import:  from my_app import views_p
    2. Add a URL to urlpatterns:  path('', views_p.home, name='home')
Class-based views_p
    1. Add an import:  from other_app.views_p import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SofiaFooty.web.urls')),
]

#TODO:
# check tournament teams when teams leave,
# fix settings file security
#  NON-ESSENTIAL add testing
#  NON-ESSENTIAL fix rounds in tournament overview
#  NON-ESSENTIAL try to add REST functionality
#  NON-ESSENTIAL try to add asynchronius functionality
#  NON-ESSENTIAL try to improve the exception handling
#  NON-ESSENTIAL add sorting to all tournaments/teams
#  NON-ESSENTIAL add toaster for eliminated teams in tournament details page
#  NON-ESSENTIAL add twitter profile and share to twitter for matches
