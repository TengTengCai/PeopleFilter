# from django.urls import paths
from django.conf.urls import url

from people import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^person_time/', views.get_person_by_time),
    url(r'^person_age/', views.get_person_by_age),
    url(r'^download/', views.out_put_excel),
    # url(r'^upload_file/', views.upload_file),

]
