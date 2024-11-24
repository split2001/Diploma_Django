from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User


# создаем свою форму, чтобы добавить email и age в существующую форму UserCreationForm
class UserRegister(UserCreationForm):
    email = forms.EmailField(label='Введите email:', required=True)
    age = forms.IntegerField(max_value=100, label='Введите возраст:', required=True)


class RecipeForm(forms.Form):
    title = forms.CharField(max_length=100,  label='Описание')
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    ingredients = forms.CharField(widget=forms.Textarea, label='Ингридиенты')
    instructions = forms.CharField(widget=forms.Textarea, label='Инструкция по приготовлению')
    image = forms.ImageField(widget=forms.ClearableFileInput)



# class Login(AuthenticationForm):
#     username = forms.CharField(max_length=10, label='Введите логин:', required=True, widget=forms.TextInput)
#     password1 = forms.CharField(min_length=8, label='Введите пароль:', required=True, widget=forms.PasswordInput)