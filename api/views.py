# api/views.py
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer, AIModelSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models_config import AI_MODELS  # Asegúrate de importar la lista estática
from .models import Conversation
from .serializers import ConversationSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
        return Response(data)

    def put(self, request):
        user = request.user
        data = request.data
        user.username = data['username']
        user.email = data['email']
        user.save()
        return Response({'message': 'Profile updated successfully'})
    
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'Profile deleted successfully'})
    
class AIModelListView(generics.ListAPIView):
    serializer_class = AIModelSerializer
    permission_classes = [AllowAny]  # Permitir acceso público

    def get_queryset(self):
        return AI_MODELS
    
class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user).order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)