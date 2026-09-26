from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from mobiles import views

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='mobiles/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Admin
    path('admin/', admin.site.urls),

    # Home
    path('', views.home, name='home'),

    # Add Mobile
    path(
        'add/',
        views.add_mobile,
        name='add_mobile'
    ),
    path('import/', views.import_mobiles, name='import_mobiles'),
    path('import/confirm/', views.confirm_import, name='confirm_import'),

    # Edit Mobile
    path(
        'mobile/<int:id>/edit/',
        views.edit_mobile,
        name='edit_mobile'
    ),

    # Delete Mobile
    path(
        'mobile/<int:id>/delete/',
        views.delete_mobile,
        name='delete_mobile'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
