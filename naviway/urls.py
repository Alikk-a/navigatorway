"""metriktrd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('mail_arh', views.arh, name='arh'),
    path('<slug:pageurl>', views.content, name='content'),
    path('teh/<int:id_cel>', views.tehnik, name='tehnik'),
    path('cource/<int:id_cource>', views.tehnikcource, name='tehnikcource'),
    path('tehtarget/', views.tehtarget, name='tehtarget'),
    path('cources/', views.cources, name='cources'),
    path('tehnik/<int:id_texnik>/', views.tehnik_one, name='tehnik_one'),
    path('cardbasic/', views.cardbasic, name='cardbasic'),
    path('registr/', views.registr, name='registr'),
    path('prof/', views.prof, name='prof'),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="text/plain")),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
