from django.urls import path

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

    path('box/<int:pk>/versions/list/', views.BoxVersionListView.as_view(), name="box-version-list"),
]