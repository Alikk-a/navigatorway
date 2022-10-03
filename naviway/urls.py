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

urlpatterns = [
    path('', views.home, name='home'),
    path('mail_arh', views.arh, name='arh'),
    path('<slug:pageurl>', views.content, name='content'),
    path('teh/<int:id_cel>', views.tehnik, name='tehnik'),
    path('tehtarget/', views.tehtarget, name='tehtarget'),
    path('tehnik/<int:id_texnik>/', views.tehnik_one, name='tehnik_one'),
    path('cardbasic/', views.cardbasic, name='cardbasic'),
    # path('change_activ2/', views.change_activ2, name='change_activ2'),
    # path('pos/<int:post_id>/', views.specific_post, name='specific_post'),
    # path('change_ex/', views.change_ex, name='change_ex'),
    # path('change_adr/', views.change_adr, name='change_adr'),
    # path('addresses.html', views.addresses, name='addresses.html'),
    # path('activity.html', views.activity, name='activity.html'),
    # path('profloss.html', views.profloss, name='profloss.html'),
    # path('exchange.html', views.exchange, name='exchange.html'),
    # path('bigtrans.html', views.bigtrans, name='bigtrans.html'),
    # path('bigtrans_filter.html', views.bigtrans_filter, name='bigtrans_filter.html'),
    # path('bigtrans_agr.html', views.bigtrans_agr, name='bigtrans_agr.html'),
    # path('bigtrans_full.html', views.bigtrans_full, name='bigtrans_full.html'),
    # path('bigtransavg_btc', views.bigtrans_szn, name='bigtransavg_btc'),
    # path('bigtransavg_eth', views.bigtranseth_szn, name='bigtransavg_eth'),
    # path('bigtrans_sum.html', views.bigtrans_sum, name='bigtrans_sum.html'),
    # path('o120522.html', views.o120522, name='o120522.html'),

]
