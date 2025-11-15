from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Todo
from .serializers import TodoSerializer


# Create your views here.
class TodoListCreateAPIView(APIView):
    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)
        serializer = TodoSerializer(instance=todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
