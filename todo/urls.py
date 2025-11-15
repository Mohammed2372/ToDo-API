from django.urls import path

from . import views


urlpatterns = [
    path("todos/", views.TodoListCreateAPIView.as_view(), name="todo-list"),
    path(
        "todos/<int:todo_id>/",
        views.TodoRetrieveUpdateDestroyAPIView.as_view(),
        name="todo-detail",
    ),
    path(
        "todos/<int:todo_id>/complete/",
        views.TodoCompletedUpdateView.as_view(),
        name="todo-complete-toggle",
    ),
]
