from django.conf.urls import url
import views

urlpatterns = [
    url(r'^profile$', views.Profile.as_view()),
]
