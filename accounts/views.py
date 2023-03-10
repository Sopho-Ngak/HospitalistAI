
# Django imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Local imports
from accounts.froms import SignupForm, LoginForm, DoctorInputForm, VerificationCodeForm, ForgetPasswordForm, SetNewPasswordForm
from accounts.models import User, VerificationCode
from utils.get_summary import get_summary_from_openai
from utils.code_generator import generate_code
from utils.send_email import send_verification_code
from django.utils.safestring import mark_safe


@login_required(login_url='login')
def home(request):
    form = DoctorInputForm()
    if request.method == 'POST':
        form = DoctorInputForm(request.POST)
        if form.is_valid():
            base_text = f"Summarize this patient note. The patient is being discharged to {form.cleaned_data.get('discharge_to')}, notice that in the response.\n"
            patient_notes = form.cleaned_data.get('patient_notes')
            add_more = form.cleaned_data.get('add_more')

            if add_more:
                patient_notes += add_more

            base_text += ".\nPatient's note :\n"+patient_notes

            summary = get_summary_from_openai(base_text)
            
            form = DoctorInputForm()
            context = {'form': form, 'summary': mark_safe(summary)}
            return render(request, 'home.html', context)
    #summary = 'The patient is a 37-year-old female with a history of ESRD status post renal transplant, diabetes mellitus, and hypertension. She was<br>'
    context = {'form': form,'hide':True}
    
    return render(request, 'home.html', context)


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.instance.set_password(form.cleaned_data.get('password'))
            form.save()
            return redirect('activate')
    context = {'form': form}
    return render(request, 'signup.html', context)


def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    form = LoginForm()
    try:
        activation_message = request.session.pop('activation_message')
    except:
        activation_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(
                    request, 'Username/email or password is incorrect')
                return redirect('login')
    return render(request, 'login.html', {'form': form, 'activation_message': activation_message})


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('dashboard')


def dashboard(request):
    return render(request, 'dashboard.html')


def activate_account(request):
    form = VerificationCodeForm()
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                user_code = VerificationCode.objects.get(code=code)
                user_code.user.is_active = True
                user_code.user.save()
                request.session['activation_message'] = 'Account activated successfully'
                return redirect('login')
            except VerificationCode.DoesNotExist:
                messages.error(request, 'Invalid code')
                return render(request, 'activate_account.html', {'form': form})
    return render(request, 'activate_account.html', {'form': form})


def reset_password(request):
    form = ForgetPasswordForm()
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                user_code = VerificationCode.objects.create(
                    user=user, code=generate_code())
                send_verification_code(user.username, email, user_code.code)
                return redirect('reset-password-confirm')
            except User.DoesNotExist:
                messages.error(
                    request, 'Sorry, we could not find an account with this email address')
                return render(request, 'activate_account.html', {'form': form, 'reset_password_form': True})
    return render(request, 'activate_account.html', {'form': form, 'reset_password_form': True})


def reset_password_confirm(request):
    form = VerificationCodeForm()
    password_conform = True
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                user_code = VerificationCode.objects.get(code=code)
                if user_code.is_used:
                    return redirect('reset-password')
                request.session['user_id'] = str(user_code.user.id)
                user_code.delete()
                return redirect('reset-password-complete')
            except VerificationCode.DoesNotExist:
                messages.error(request, 'Invalid code')
                return render(request, 'activate_account.html', {'form': form, 'password_conform': password_conform})
    return render(request, 'activate_account.html', {'form': form, 'password_conform': password_conform})


def reset_password_complete(request):
    form = SetNewPasswordForm()
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user_id = request.session.pop('user_id', None)
            password = form.cleaned_data.get('password2')
            try:
                user = User.objects.get(id=str(user_id))
                user.set_password(password)
                user.is_active = True
                user.save()
                messages.success(
                    request, 'Your Password has been updated successfully. You can now login')
                return render(request, 'activate_account.html', {'password_updated': True})
            except:
                return redirect('reset-password')
        else:
            return render(request, 'activate_account.html', {'form': form, 'reset_password_complete': True})

    return render(request, 'activate_account.html', {'form': form, 'reset_password_complete': True})
