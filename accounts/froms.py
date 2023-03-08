from django import forms
from accounts.models import User


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(
        widget=forms.PasswordInput, label='Confirm Password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    class Meta:
        model = User
        fields = ['email', 'username', 'full_name', 'password']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class DoctorInputForm(forms.Form):
    discharge_to = forms.CharField(label='Where is the patient getting discharged to?', widget=forms.TextInput(
        attrs={'placeholder': 'e.g: home', 'class': 'form-control'}), required=True)
    patient_notes = forms.CharField(label='Enter the patient\'s most recent progress note', widget=forms.Textarea(
        attrs={
        'placeholder': 'e.g \nPatient is a 37-year-old female with past medical history of ESRD status post renal transplant...', 
        'class': 'form-control', 
        'rows': 10, 
        'id': 'my-textarea-id'
        }), required=True)
    add_more = forms.CharField(label='Tell HospitalistAI if there is any additional information it should consider or leave the field blank if there is not.', widget=forms.TextInput(
        attrs={
        'placeholder': 'e.g: with more details', 
        'class': 'form-control', 
        "place_holder": "Be more specific based on your choice", 
        }), required=False)
    

    class Meta:
        fields = ['discharge_at', 'patient_notes']


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
                             'placeholder': 'e.g:example@gmail.com', 'class': 'form-control'}), required=True)


class SetNewPasswordForm(forms.Form):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), required=True)

    def clean_password2(self):
        password = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2


class VerificationCodeForm(forms.Form):
    code = forms.CharField(label='Verification code', widget=forms.TextInput(
        attrs={'placeholder': 'e.g: 123456', 'class': 'form-control'}), required=True)
