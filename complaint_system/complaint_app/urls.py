from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('',         views.login_view,    name='home'),
    path('register/', views.register_view, name='register'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),

    # User
    path('dashboard/',              views.dashboard,          name='dashboard'),
    path('complaint/submit/',       views.submit_complaint,   name='submit_complaint'),
    path('complaint/my/',           views.my_complaints,      name='my_complaints'),
    path('complaint/<int:pk>/',     views.complaint_detail,   name='complaint_detail'),
    path('notifications/',          views.notifications_view, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_read'),

    # Admin
    path('admin-dashboard/',                        views.admin_dashboard,        name='admin_dashboard'),
    path('admin-dashboard/complaints/',             views.admin_complaints,       name='admin_complaints'),
    path('admin-dashboard/complaint/<int:pk>/',     views.admin_complaint_detail, name='admin_complaint_detail'),
    path('admin-dashboard/users/',                  views.admin_users,            name='admin_users'),

    # API
    path('api/unread-count/', views.api_unread_count, name='api_unread_count'),
]
