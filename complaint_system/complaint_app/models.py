from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='⚠️')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('investigating', 'Investigating'),
        ('resolved',    'Resolved'),
        ('rejected',    'Rejected'),
    ]

    PRIORITY_CHOICES = [
        ('low',    'Low'),
        ('medium', 'Medium'),
        ('high',   'High'),
        ('urgent', 'Urgent'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title       = models.CharField(max_length=200)
    description = models.TextField()
    location    = models.CharField(max_length=255, blank=True)
    priority    = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    attachment  = models.ImageField(upload_to='complaints/', blank=True, null=True)
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title} — {self.user.username}"

    @property
    def status_color(self):
        return {
            'pending':      '#f59e0b',
            'investigating': '#3b82f6',
            'resolved':     '#10b981',
            'rejected':     '#ef4444',
        }.get(self.status, '#6b7280')


class ComplaintUpdate(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='updates')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    message    = models.TextField()
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, blank=True)
    timestamp  = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Update on #{self.complaint.id} by {self.updated_by.username}"


class Notification(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message   = models.TextField()
    is_read   = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    link      = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notif for {self.user.username}: {self.message[:40]}"
