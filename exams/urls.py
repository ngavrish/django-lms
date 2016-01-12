from django.conf.urls import url

from exams import views


urlpatterns = [
    url(r'^$', views.list_exams, name='list_exams'),
    url(r'^create$', views.create_exam, name='create_exam'),
    url(r'^(\d+)$', views.edit_exam, name='edit_exam'),
    url(r'^(\d+)/scores$', views.view_scores, name='view_scores'),
    url(r'^(\d+)/s$', views.view_exam, name='view_exam'),
    url(r'^(\d+)/take$', views.take_exam, name='take_exam'),
    url(r'^(\d+)/result$', views.view_result, name='view_result'),
]