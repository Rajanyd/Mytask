from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.contrib.auth import logout as auth_logout

class RegisterView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        passcode = request.data.get('passcode')
        user = User.objects.filter(username=username, passcode=passcode).first()
        if user:
            request.session['user_id'] = user.id
            return redirect('list_tasks')
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class AddTaskView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_task.html')

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.session['user_id'])
            return redirect('list_tasks')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListTasksView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        tasks = Task.objects.filter(user_id=user_id)

        search_query = request.GET.get('search', '')
        if search_query:
            tasks = tasks.filter(title__icontains=search_query)

        sort_by = request.GET.get('sort_by', 'due_date')
        tasks = tasks.order_by(sort_by)

        # Task count
        task_count = tasks.count()

        return render(request, 'tasks.html', {'tasks': tasks, 'task_count': task_count})

class SendReminderView(APIView):
    def post(self, request, *args, **kwargs):
        task_id = request.data.get('task_id')
        task = Task.objects.get(id=task_id)
        send_mail(
            'Task Reminder',
            f'Reminder: Your task "{task.title}" is due on {task.due_date}.',
            'from@example.com',
            [task.user.email],
            fail_silently=False,
        )
        return Response({"message": "Reminder sent"}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        request.session.flush()  # Clears session data
        return redirect('login')