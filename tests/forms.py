from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Test


test_complexity = (
    (1, 'hard'),
    (2, 'normal'),
    (3, 'easy')
)

class CreateTestForm(forms.ModelForm):
    name = forms.CharField(max_length=250)
    complexity = forms.IntegerField()

    class Meta:
        model = Test
        fields = ('name', 'complexity')

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        try:
            test = Test.objects.exclude(pk=self.instance.pk).get(name=name)
        except Test.DoesNotExist:
            return name
        raise forms.ValidationError('Name for Test "%s" is already in use.' % test)