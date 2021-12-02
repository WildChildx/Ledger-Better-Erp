from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('studentLogin', views.studentLogin),
    path('studentDash', views.studentDash),
    path('createStudent', views.createStudent),
    path('teacher', views.teacher),
    path('admin', views.admin),
    path('teacher-dashboard', views.teacher_dashboard),
    path('admin-dashboard', views.admin_dashboard),
    path('acceptUser', views.acceptUser),
    path('rejectUser', views.rejectUser),

]
