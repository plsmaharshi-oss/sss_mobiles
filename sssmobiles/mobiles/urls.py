from django.contrib import admin
from django.urls import path
from mobiles import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('add/', views.add_mobile, name='add_mobile'),

    path('mobile/<int:id>/edit/', views.edit_mobile, name='edit_mobile'),

    path('mobile/<int:id>/delete/', views.delete_mobile, name='delete_mobile'),
]