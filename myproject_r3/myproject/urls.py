from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users import views

urlpatterns = [
    path('',views.TopView.as_view(),name='top'), 
    path('users/',include('users.urls')),
    path('coordination_app/',include('coordination_app.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
