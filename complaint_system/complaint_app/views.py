from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone

from .models import Complaint, Category, ComplaintUpdate, Notification
from .forms import RegisterForm, LoginForm, ComplaintForm, UpdateStatusForm


# ─── Helpers ──────────────────────────────────────────────────────────────────

def is_admin(user):
    return user.is_staff or user.is_superuser


def add_notification(user, message, link=''):
    Notification.objects.create(user=user, message=message, link=link)


# ─── Auth ─────────────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.first_name}! Your account is ready.')
        return redirect('dashboard')
    return render(request, 'complaint_app/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name or user.username}!')
        return redirect('admin_dashboard' if is_admin(user) else 'dashboard')
    return render(request, 'complaint_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─── User Views ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    complaints = Complaint.objects.filter(user=request.user)
    stats = {
        'total':        complaints.count(),
        'pending':      complaints.filter(status='pending').count(),
        'investigating': complaints.filter(status='investigating').count(),
        'resolved':     complaints.filter(status='resolved').count(),
    }
    recent      = complaints[:5]
    unread_notifs = request.user.notifications.filter(is_read=False).count()
    return render(request, 'complaint_app/dashboard.html', {
        'stats': stats, 'recent': recent, 'unread_notifs': unread_notifs
    })


@login_required
def submit_complaint(request):
    form = ComplaintForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        complaint = form.save(commit=False)
        complaint.user = request.user
        complaint.save()
        # Notify all admins
        for admin_user in User.objects.filter(is_staff=True):
            add_notification(
                admin_user,
                f'New complaint #{complaint.id} submitted by {request.user.username}: "{complaint.title}"',
                link=f'/admin-dashboard/complaint/{complaint.id}/'
            )
        messages.success(request, f'Complaint #{complaint.id} submitted successfully!')
        return redirect('my_complaints')
    return render(request, 'complaint_app/submit_complaint.html', {'form': form})


@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user)
    status_filter = request.GET.get('status', '')
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    return render(request, 'complaint_app/my_complaints.html', {
        'complaints': complaints,
        'status_filter': status_filter,
    })


@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, user=request.user)
    updates   = complaint.updates.all()
    return render(request, 'complaint_app/complaint_detail.html', {
        'complaint': complaint, 'updates': updates
    })


@login_required
def notifications_view(request):
    notifs = request.user.notifications.all()
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'complaint_app/notifications.html', {'notifs': notifs})


@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return JsonResponse({'status': 'ok'})


# ─── Admin Views ──────────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    all_complaints = Complaint.objects.select_related('user', 'category').all()
    stats = {
        'total':        all_complaints.count(),
        'pending':      all_complaints.filter(status='pending').count(),
        'investigating': all_complaints.filter(status='investigating').count(),
        'resolved':     all_complaints.filter(status='resolved').count(),
        'rejected':     all_complaints.filter(status='rejected').count(),
        'users':        User.objects.filter(is_staff=False).count(),
    }
    by_category = (
        Category.objects.annotate(count=Count('complaint'))
        .values('name', 'icon', 'count')
        .order_by('-count')
    )
    recent = all_complaints[:10]
    unread_notifs = request.user.notifications.filter(is_read=False).count()
    return render(request, 'complaint_app/admin_dashboard.html', {
        'stats': stats, 'by_category': by_category,
        'recent': recent, 'unread_notifs': unread_notifs,
    })


@login_required
@user_passes_test(is_admin)
def admin_complaints(request):
    complaints = Complaint.objects.select_related('user', 'category').all()
    status_filter   = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search          = request.GET.get('q', '')

    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if priority_filter:
        complaints = complaints.filter(priority=priority_filter)
    if search:
        complaints = complaints.filter(
            Q(title__icontains=search) |
            Q(user__username__icontains=search) |
            Q(description__icontains=search)
        )
    return render(request, 'complaint_app/admin_complaints.html', {
        'complaints': complaints,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'search': search,
    })


@login_required
@user_passes_test(is_admin)
def admin_complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    form      = UpdateStatusForm(request.POST or None, instance=complaint)
    updates   = complaint.updates.all()

    if request.method == 'POST' and form.is_valid():
        old_status = complaint.status
        updated    = form.save()
        note_msg   = form.cleaned_data.get('message', '')

        ComplaintUpdate.objects.create(
            complaint  = complaint,
            updated_by = request.user,
            message    = note_msg or f'Status changed to {complaint.get_status_display()}.',
            old_status = old_status,
            new_status = complaint.status,
        )
        # Notify the complaint owner
        add_notification(
            complaint.user,
            f'Your complaint #{complaint.id} status updated to "{complaint.get_status_display()}".',
            link=f'/complaint/{complaint.id}/'
        )
        messages.success(request, f'Complaint #{pk} updated.')
        return redirect('admin_complaint_detail', pk=pk)

    return render(request, 'complaint_app/admin_complaint_detail.html', {
        'complaint': complaint, 'form': form, 'updates': updates
    })


@login_required
@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.filter(is_staff=False).annotate(
        complaint_count=Count('complaints')
    ).order_by('-date_joined')
    return render(request, 'complaint_app/admin_users.html', {'users': users})


# ─── API ──────────────────────────────────────────────────────────────────────

@login_required
def api_unread_count(request):
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})
