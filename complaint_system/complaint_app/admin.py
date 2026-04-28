from django.contrib import admin
from .models import Complaint, Category, ComplaintUpdate, Notification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display  = ['id', 'title', 'user', 'category', 'status', 'priority', 'created_at']
    list_filter   = ['status', 'priority', 'category']
    search_fields = ['title', 'user__username', 'description']
    list_editable = ['status', 'priority']


@admin.register(ComplaintUpdate)
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'updated_by', 'new_status', 'timestamp']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
