from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from .models import Todo
from .serializers import (
    TodoSerializer,
    TodoDetailSerializer,
    RegisterSerializer,
    EmailLoginSerializer,
)
from .filters import TodoFilter


# Create your views here.
## Todo
class TodoListCreateAPIView(generics.ListCreateAPIView):
    # queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filterset_class = TodoFilter
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = ["title", "description"]
    ordering_fields = ["date_created", "title", "completed"]
    ordering = ["-date_created"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Todo.objects.all()
        return Todo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # NOTE: changed to user generics instead of APIView, so no need to use, as they are built and better.
    # def get(self, request):
    #     todos = Todo.objects.all()
    #     serializer = TodoSerializer(todos, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id, owner=request.user)
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data)

    def put(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id, owner=request.user)
        serializer = TodoDetailSerializer(instance=todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id, owner=request.user)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoCompletedUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id, owner=request.user)

        todo.completed = not todo.completed
        todo.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)


## User Authentication
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class EmailLoginView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = EmailLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user = validated_data.pop("user")
        login(request, user)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
