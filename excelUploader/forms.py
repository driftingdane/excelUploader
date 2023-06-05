from allauth.account.forms import (AddEmailForm, ChangePasswordForm, LoginForm,
                                   ResetPasswordForm, ResetPasswordKeyForm,
                                   SetPasswordForm, SignupForm, UserTokenForm)
from django import forms
from django.utils.translation import gettext_lazy as _


# Inherit Allauth forms and customise them

class MyCustomUserTokenForm(UserTokenForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomUserTokenForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'


class MyCustomResetPasswordKeyForm(ResetPasswordKeyForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomResetPasswordKeyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'


class MyCustomChangePasswordForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomChangePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'


class MyCustomAddEmailForm(AddEmailForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomAddEmailForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'


class MyCustomSerPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomSerPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'


class MyCustomResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomResetPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'


class MyCustomLoginForm(LoginForm):
    #remember = forms.CharField(label=_("Remember Me"), required=False, widget=forms.CheckboxInput(attrs={
        #'class': 'form-check-input',
    #}))

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember')
        if remember_me:
            self.request.session.set_expiry(1209600)  # 2 weeks
        else:
            self.request.session.set_expiry(0)  # session cookie expires when user closes the browser

    def __init__(self, *args, **kwargs):
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if not isinstance(visible.field.widget, forms.CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-control mb-3'


class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Username',
                                 widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'
