import json

from algoliasearch_django import raw_search
from django.contrib.auth import authenticate
from django.views.decorators import csrf
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, authtoken
from rest_framework import generics
from . import serializers
from django import db
from . import models
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import permissions as custom_permission
from django.http import JsonResponse


@csrf.csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    """Handles POST request to register a user"""
    user_data = request.data
    try:
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        del user_data['confirm_password']
    except KeyError:
        return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = serializers.UserSerializer(data=user_data)
    if serializer.is_valid():
        try:
            serializer.save()
        except db.IntegrityError:
            return Response({'error': 'Email is already in use'}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid input'}, status=status.HTTP_409_CONFLICT)


@csrf.csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    """Handle POST request to login a user"""
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Email or password are not correct'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_401_UNAUTHORIZED)
    token, _ = authtoken.models.Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)


class ComposeList(generics.ListCreateAPIView):
    """class which defines the views for the compose stories"""
    serializer_class = serializers.ComposeSerializer

    def get_queryset(self):
        return self.request.user.composer.all()


class ComposeDetail(generics.RetrieveUpdateDestroyAPIView):
    """class which defines views for the compose stores details"""
    permission_classes = [custom_permission.ComposeOwnerOnly]
    queryset = models.Compose.objects.all()
    serializer_class = serializers.ComposeSerializer


@csrf.csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def logout(request):
    """Handles POST requests to log a user out."""
    request.user.auth_token.delete()
    return Response({"message": f"Logged out {request.user.email}."},
                    status=status.HTTP_200_OK)


@csrf.csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def contact(request):
    """Handles POST requests to save user issues"""
    contact_data = request.data
    serializer = serializers.ContactSerializer(contact_data)
    if serializer.is_valid():
        try:
            serializer.save()
        except Exception as e:
            return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"error": "server is not responding"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search(request):
    """Search story by title """
    search_query = request.GET.get('title')
    params = {"hitsPerPage": 5
              }
    response = raw_search(models.Compose, search_query, params)
    if response['nbHits'] == 0:
        return JsonResponse({"error": "No search Found"}, status=status.HTTP_404_NOT_FOUND)
    return JsonResponse(response, status=status.HTTP_200_OK)
