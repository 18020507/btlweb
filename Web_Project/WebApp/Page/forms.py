from django import forms
from django.contrib.auth.models import User
from .models import Customer


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class AddressInputForm(forms.ModelForm):
    address = forms.CharField(label='Address', max_length=1000, widget=forms.TextInput(attrs={"class": "form-control"}))


class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={"class": "textbox"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={"class": "textbox"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "textbox"}))
    password2 = forms.CharField(label='Input Password Again',
                                widget=forms.PasswordInput(attrs={"class": "textbox"}))
    fullname = forms.CharField(label='Fullname', max_length=30, widget=forms.TextInput(attrs={"class": "textbox"}))
    phone = forms.CharField(label='Phone_Number', max_length=11,
                            widget=forms.TextInput(attrs={"class": "textbox"}))

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Invalid Password")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username already exist")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("Email already exist")

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password1'])
        Customer.objects.create(user=user, phone=self.cleaned_data['phone'], name=self.cleaned_data['fullname'])
