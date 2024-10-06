
from django.contrib import admin
from django.urls import path
from chat import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name= 'home'),
    path('<str:room>/', views.room, name= 'room'),
    path('checkview/', views.checkview, name= 'salle'),
    path('send', views.send, name= 'send'),
    path('getMessages/<str:room>/', views.getMessages, name= 'getMessages'),
    path('run-script/', views.run_script, name='run-script')
]
