from django.urls import path
from accounts.views import (user_login, signup, home, user_logout, dashboard,
                            activate_account, reset_password, reset_password_complete, reset_password_confirm)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login/', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('home/', home, name='home'),
    path('logout/', user_logout, name='logout'),
    path('activate/', activate_account, name='activate'),
    path('reset-password/', reset_password, name='reset-password'),
    path('reset-password/complete/', reset_password_complete,
         name='reset-password-complete'),
    path('reset-password/confirm/', reset_password_confirm,
         name='reset-password-confirm'),

]
