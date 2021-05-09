from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^health-check', views.health_check),
    url(r'^create-yaml', views.create_yaml),
    url(r'^add-cluster', views.add_cluster),
    url(r'^deploy-operator-resources', views.deploy_operator_resources),
    url(r'^deploy-resources', views.deploy_resources),
    url(r'^delete-resources', views.delete_resource),
    url(r'^delete-operator-resources', views.delete_operator_resources),
]
