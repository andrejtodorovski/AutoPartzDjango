from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import Form, CharField, PasswordInput, EmailField, ValidationError, ModelForm

from autopartz.models import CustomUser, Delivery, Part


class RegistrationForm(Form):
    username = CharField(max_length=150)
    password = CharField(widget=PasswordInput)
    full_name = CharField(max_length=100)
    email = EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            password=self.cleaned_data.get('password')
        )
        custom_user = CustomUser.objects.create(
            user=user,
            full_name=self.cleaned_data.get('full_name'),
            email=self.cleaned_data.get('email')
        )
        return custom_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'


class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'


class DeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        exclude = ['order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'


class PartForm(ModelForm):
    class Meta:
        model = Part
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'