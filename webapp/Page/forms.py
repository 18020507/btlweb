from django import forms
from django.contrib.auth.models import User
from .models import Custumer
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
#     address = forms.CharField(max_length=50, required=True)
#     age = forms.CharField(max_length=2, required=True)
#     sex = forms.CharField(max_length=3, required=False)
#     phone = forms.CharField(max_length=20, required=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(label='Input Password Again', widget=forms.PasswordInput(attrs={"class":"form-control"}))
    fullname = forms.CharField(label='Fullname', max_length=30, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Address', max_length=30, widget=forms.TextInput(attrs={"class":"form-control"}))
    age = forms.IntegerField(label='Age', max_value=100, min_value=2, widget=forms.NumberInput(attrs={"class":"form-control"}))
    sexual = forms.CharField(label="Sexual", max_length=3, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    phone = forms.CharField(label='Phone_Number', max_length=11, widget=forms.TextInput(attrs={"class":"form-control"}))

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
        customer = Custumer.objects.create(user=user, age=self.cleaned_data['age'], address=self.cleaned_data['address'], phone=self.cleaned_data['phone'], name=self.cleaned_data['fullname'])