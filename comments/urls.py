from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:product_id>/', views.add_comment, name='add_comment'),
    path('reply/<int:comment_id>/', views.add_reply, name='add_reply'),
]
