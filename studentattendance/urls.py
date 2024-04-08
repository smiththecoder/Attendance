from django.urls import path
from .views import home,main,res

urlpatterns = [
    path('',home),
    path('main',main),
    path('result',res)
]
