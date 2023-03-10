from accounts.models import User
from django.db.models import Q

def add_variable_to_context(request):
    if request.user.is_authenticated:
        label = ["Total Users", "Active Accounts", "Inactive Accounts", "Total Admins"]
        total_users = User.objects.filter(is_admin=False).count()
        active_accounts = User.objects.filter(is_active=True, is_admin=False).count()
        inactive_accounts = User.objects.filter(is_active=False, is_admin=False).count()
        total_admins = User.objects.filter(is_admin=True).count()
        value = [
            total_users, 
            active_accounts, 
            inactive_accounts, 
            total_admins
            ]
        return {
            'chart_labels': label,
            'chart_label': label,
            'chart_data': value,
            'total_users': total_users,
            'active_accounts': active_accounts,
            'inactive_accounts': inactive_accounts,
            'total_admins': total_admins,
        }

    return {}
    