from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError


class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name',)

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
        user.is_active = True
        user.save()

        return user


class SignInForm(forms.Form):
    email_or_username = forms.CharField(required=True)
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput
    )

    def clean(self, *args, **kwargs):
        data = self.data
        email_or_username = data['email_or_username']
        User = get_user_model()

        try:
            if '@' in email_or_username:
                user = User.objects.get(email=email_or_username)
            else:
                user = User.objects.get(username=email_or_username)
            user = authenticate(username=user.username, password=data['password'])
            if not user or not user.is_active:
                raise ValidationError(u'Username/email or password incorrect')
        except User.DoesNotExist:
            raise ValidationError(u'Username/email or password incorrect')

        self.cleaned_data['user'] = user

        return super(SignInForm, self).clean(*args, **kwargs)
