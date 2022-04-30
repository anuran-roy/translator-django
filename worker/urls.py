"""translator URL Configuration

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
# from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("translate_sample/", views.translate_sample, name="translate_sample"),
    # path("create_project/", views.create_project, name="create_project"),
    # path("project/<int:pk>/", views.view_project, name="view_project"),
    path("process/", views.process_input, name="process_input"),
    path("projects/", views.ListProjects.as_view(), name="projects"),
    path("projects/new/", views.CreateProject.as_view(), name="create_project"),
    path(
        "projects/<int:project_pk>/", views.get_project_details, name="project_details"
    ),
    path(
        "projects/<int:project_pk>/modify_translation/",
        views.modify_translation,
        name="modify_translation",
    ),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("project/<int:pk>/tasks/<int:tasks_pk>", views.view_translation, name="view_translations"),
]
