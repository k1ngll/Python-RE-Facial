from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from gestor import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin-area/', admin.site.urls),
    path('', views.login_gestor, name='login'),
    path('cadastro/', include('cadastro_face.urls')),  # ou o nome real do app
    path('gestor/', include('gestor.urls')),  # <-- usa o nome do app (gestor)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
