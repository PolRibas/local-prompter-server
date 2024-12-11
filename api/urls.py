from django.urls import path
from .views import (
    AIModelDetailView,
    RegisterView, 
    ProfileView, 
    AIModelListView, 
    ConversationListCreateView, 
    UserDetailView, 
    UserListView,
    ChatView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('models/', AIModelListView.as_view(), name='ai_models'), 
    path('models/<str:code>/', AIModelDetailView.as_view(), name='ai_model_detail'),
    path('conversations/', ConversationListCreateView.as_view(), name='conversations'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('chats/', ChatView.as_view(), name='chat_view'),
]