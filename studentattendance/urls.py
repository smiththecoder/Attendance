from django.urls import path
from .views import home,main,res,apid

urlpatterns = [
    path('',home),
    path('main',main),
    path('result',res),
    path('api/<str:roll>',apid)
]
