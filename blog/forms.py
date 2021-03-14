from django import forms
from blog.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(help_text="Format: YYYY-MM-DD")
    email = forms.EmailField(label="Email address")
    first_name = forms.CharField()
    last_name = forms.CharField()
    image = forms.ImageField(label="Profile picture", widget=forms.FileInput)
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES)
    country = forms.ChoiceField(choices=Profile.COUNTRY_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'birth_date', 'country', 'gender', 'image', 'password1', 'password2']


class Register1Form(forms.ModelForm):
    email = forms.EmailField(label="Email address")
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class Register2Form(forms.ModelForm):
    country = forms.ChoiceField(choices=Profile.COUNTRY_CHOICES)
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES)
    birth_date = forms.DateField(help_text="Format: YYYY-MM-DD")
    image = forms.ImageField(label="Profile picture", widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['country', 'gender', 'birth_date', 'image']


class Register3Form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileImgForm(forms.ModelForm):
    image = forms.ImageField(label="", required=False, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['image']


class ProfileBgForm(forms.ModelForm):
    background = forms.ImageField(
        label="", required=False, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['background']


class ProfileBioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']


class ProfileIntroForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['country', 'birth_date', 'gender']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'gender', 'birth_date',
                  'country', 'image', 'background']


class UpdatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
