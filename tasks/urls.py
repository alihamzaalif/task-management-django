from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,test
urlpatterns = [
    # path('show-task/', show_task),
    path('manager-dashboard/', manager_dashboard),
    path('user-dashboard/', user_dashboard),
    path('test/', test)
]