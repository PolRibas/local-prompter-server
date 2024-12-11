# api/views.py
from rest_framework import generics, permissions, filters
from django.contrib.auth.models import User
from .serializers import UserSerializer, AIModelSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models_config import AI_MODELS  # Asegúrate de importar la lista estática
from .models import Conversation
from .serializers import ConversationSerializer
from rest_framework import status
from integrations.AI.ai_factory import get_ai_instance
from django.shortcuts import get_object_or_404
from .models import ChatSession, ConversationMessage
from .serializers import ChatSessionSerializer

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

class AIModelDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, code):
        # Buscar el modelo con el code dado
        for m in AI_MODELS:
            if m['id'] == code:  # o si el campo es 'code' y no 'id', ajústalo
                return Response(m)
        return Response({'detail': 'Modelo no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user).order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

class UserDetailView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if request.user.username != 'grizzly':
            return Response({'detail': 'No tienes permiso para borrar usuarios.'}, status=status.HTTP_403_FORBIDDEN)

        # Verificar que el usuario a borrar existe
        instance = self.get_object()  # Esto retornará 404 si no existe el usuario con pk dado
        # Si llegamos aquí, el usuario existe
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Espera:
        {
          "chat_id": optional,
          "model_code": optional,
          "message": "Hola, ¿cómo estás?" 
        }
        Si no se da chat_id, se crea uno nuevo con el model_code dado (o por defecto).
        Si se da chat_id, se usa ese chat y su model_code.
        Obtiene el historial de la base de datos, añade el nuevo mensaje del usuario,
        llama a la IA y añade la respuesta del asistente.
        Retorna el chat_id y la lista actualizada de mensajes.
        """
        chat_id = request.data.get('chat_id')
        model_code = request.data.get('model_code', 'Llama-3.1-8B-Instruct')
        user_message = request.data.get('message')
        if not user_message:
            return Response({'detail': 'Falta message.'}, status=status.HTTP_400_BAD_REQUEST)

        if chat_id:
            chat_session = get_object_or_404(ChatSession, pk=chat_id, user=request.user)
            # Usar el model_code del chat ya existente
            model_code = chat_session.model_code
        else:
            # Crear un nuevo chat
            chat_session = ChatSession.objects.create(user=request.user, model_code=model_code)

        # Obtener historial
        history = chat_session.messages.order_by('timestamp')
        messages = []
        # Cargar mensajes previos en el formato esperado por la IA
        # Opcionalmente podrías añadir un system prompt inicial
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        # Añadir el nuevo mensaje del usuario
        messages.append({"role": "user", "content": user_message})

        # Llamar a la IA
        try:
            ai = get_ai_instance(model_code)
            response_text = ai.generate_response(messages)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Error interno al generar respuesta.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Guardar el mensaje del usuario y la respuesta
        ConversationMessage.objects.create(
            chat_session=chat_session,
            role='user',
            content=user_message
        )
        ConversationMessage.objects.create(
            chat_session=chat_session,
            role='assistant',
            content=response_text
        )

        # Retornar el chat con el historial actualizado
        serializer = ChatSessionSerializer(chat_session)
        return Response(serializer.data)