from django.urls import path
from . import views

app_name = "recommendations"

urlpatterns = [
    path("gift/", views.recommend_gift, name="gift"),
]
