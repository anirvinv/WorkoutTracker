from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class ExerciseForm(forms.Form):
    name = forms.CharField(label='Exercise Name',
                           required=True, max_length=100)
    volume = forms.IntegerField(label='Total Reps', required=True, min_value=1)
    rpe = forms.FloatField(label='RPE', required=True,
                           max_value=10, min_value=1)


class StatsForm(forms.Form):
    height = forms.IntegerField(
        label="height", required=True, min_value=1)
    weight = forms.IntegerField(label="weight", required=True, min_value=1)
