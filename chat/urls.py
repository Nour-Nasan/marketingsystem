from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('<int:conversation_id>/', views.chat_detail, name='chat_detail'),
    path('start/<int:shop_id>/', views.start_conversation, name='start_conversation'),
    path('delete/<int:conversation_id>/', views.confirm_delete_conversation, name='confirm_delete_conversation'),
]
