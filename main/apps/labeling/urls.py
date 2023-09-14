
from django.urls import path

from apps.labeling import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('create_project', views.create_project, name='create_project'),
    path('project_list', views.project_list, name='project_list'),
    path('review', views.review, name='review'),
    path('method_list', views.method_list, name='method_list'),
    path('code_table', views.code_table, name='code_table'),
    path('post_pos', views.post_pos, name='post_pos'),
    path('post_neg', views.post_neg, name='post_neg'),
    path('ques_list', views.ques_list, name='ques_list'),
    path('post_ques', views.post_ques, name='post_ques'),
    path('export_csv', views.export_csv, name='export_csv'),

    path('lc_index', views.lc_index, name='lc_index'),
    path('lc_review', views.lc_review, name='lc_review'),
    path('lc_project_list', views.lc_project_list, name='lc_project_list'),
    path('create_lc_project', views.create_lc_project, name='create_lc_project'),
    path('class_list', views.class_list, name='class_list'),
    path('post_pos_class', views.post_pos_class, name='post_pos_class'),
    path('post_neg_class', views.post_neg_class, name='post_neg_class'),
    path('post_del_class', views.post_del_class, name='post_del_class'),
]
