from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError


class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        password_field = self.fields['password']
        password_field.widget = forms.PasswordInput()

        email_field = self.fields['email']
        email_field.required = True

    def clean(self, *args, **kwargs):
        data = self.data

        if not data['password'] == data['confirm_password']:
            self._errors['confirm_password'] = (u'Passwords do not match', )
        return super(SignUpForm, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        user = super(SignUpForm, self).save(commit=False)

        user.set_password(self.cleaned_data['password'])
        user.save()

        return user
