from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import MyAccount

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=20, help_text='Write your username.')

    class Meta:
        model = MyAccount
        fields = ('username', 'password1', 'password2',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = MyAccount.objects.exclude(pk=self.instance.pk).get(username=username)
        except MyAccount.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % account)


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = MyAccount
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid login")


