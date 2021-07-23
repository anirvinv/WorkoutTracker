from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
class ExerciseForm(forms.Form):
    name = forms.CharField(label='Exercise Name',required=True, max_length=100)
    volume = forms.IntegerField(label='Total Reps', required=True)
    