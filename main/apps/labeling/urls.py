
from django.urls import path

from apps.labeling import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('create_project', views.create_project, name='create_project'),
    path('project_list', views.project_list, name='project_list'),
    path('review', views.review, name='review'),
    path('method_list', views.method_list, name='method_list'),
    path('code_table', views.code_table, name='code_table'),
]
