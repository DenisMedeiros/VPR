from django import forms
from django.contrib.auth.models import User

from . import models

class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure all fields have class = form-control.
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] += ' form-check-input'                

class LoginForm(BootstrapForm):

    username = forms.CharField(label='Username', max_length=150,  widget=forms.TextInput(
        attrs={'required': True, 'placeholder': 'Username'}
        )
    )

    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(
        attrs={'required': True, 'placeholder': 'Password',}
        )
    )

    remember = forms.BooleanField(label='Remember Me', required=False, widget=forms.CheckboxInput(
        attrs={'required': False, 'class': 'form-check-input'}
        )
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Create captcha field only if keys are defined.
    #     if settings.RECAPTCHA_PUBLIC_KEY and settings.RECAPTCHA_PRIVATE_KEY:
    #         self.fields['captcha'] = ReCaptchaField(widget=ReCaptchaV2Checkbox(
    #             attrs={
    #                 'data-theme': 'light',
    #                 'data-size': 'normal',
    #                 'required': True
    #             },
    #         ))  

class BoxForm(forms.ModelForm, BootstrapForm):
   
    class Meta:
        model = models.Box
        fields = ['name', 'description', 'public', ] 

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.downloads = 0
        instance.last_download_at = None
        if commit:
            instance.save()
        return instance

class BoxVersionForm(forms.ModelForm, BootstrapForm):
   
    class Meta:
        model = models.BoxVersion
        fields = ['name', 'kind', 'description', 'file']


    def clean_file(self, *args, **kwargs):
        if not self.files.get('file'):
            return None
        return self.files.get('file')

    def save(self, commit=False, *args, **kwargs):
        self.instance = super().save(*args, **kwargs, commit=False)
        # If file is None, delete it (the user wanted to remove it).
        if self.cleaned_data['file'] is None:
            self.instance.file = None
        if commit:
            self.instance.save()            
        return self.instance