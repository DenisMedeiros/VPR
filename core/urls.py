from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'core'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('', views.HomeView.as_view(), name="home"),

    path('box/create/', views.BoxCreateView.as_view(), name="box-create"),
    path('box/edit/<int:pk>/', views.BoxEditView.as_view(), name='box-edit'),
    path('box/list/', views.BoxListView.as_view(), name="box-list"),
    path('box/delete/', views.HomeView.as_view(), name="box-delete"),
    path('box/details/', views.HomeView.as_view(), name="box-details"),

    path('box/<int:box>/version/add/', views.BoxVersionCreateView.as_view(), name="box-version-add"),
    path('box/<int:box>/version/list/', views.BoxVersionListView.as_view(), name="box-version-list"),
    path('box/<int:box>/version/edit/<int:pk>/', views.BoxVersionEditView.as_view(), name="box-version-edit"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)