from django.urls import path
from .views import RegisterView, LoginView, AddTaskView, ListTasksView,SendReminderView,LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', LoginView.as_view(), name='login'),
    path('tasks/add/', AddTaskView.as_view(), name='add_task'),
    path('tasks/', ListTasksView.as_view(), name='list_tasks'),
    path('tasks/send_reminder/', SendReminderView.as_view(), name='send_reminder'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
