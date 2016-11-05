from django.contrib import admin
from django import forms
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm


class UniqueEmailFormMixin:
    '''
    A mixin that enforces the uniqueness, relative to the User model,
    of an 'email' field in the form it's mixed-in with.

    Taken from https://gist.github.com/gregplaysguitar/1184995.
    '''

    def clean_email(self):
        qs = User.objects.filter(email=self.cleaned_data['email'])
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.count():
            raise forms.ValidationError(
                'That email address is already in use.'
            )
        else:
            return self.cleaned_data['email']


class CustomUserCreationForm(forms.ModelForm, UniqueEmailFormMixin):
    '''
    A substitute for django.contrib.auth.forms.UserCreationForm which
    doesn't ask for information about new users that's irrelevant
    to how the application works.
    '''

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email',)

    def generate_username(self, email, max_attempts=100):
        '''
        Generate a unique username based on the given email address
        by slugifying the first several characters of the username
        part of the email. If needed, a number is added at the end
        to avoid conflicts with existing usernames.
        '''

        basename = slugify(email.split('@')[0])[:15]
        for i in range(max_attempts):
            if i == 0:
                username = basename
            else:
                username = '{}{}'.format(basename, i)
            if not User.objects.filter(username=username).exists():
                return username
        raise Exception(
            'unable to generate username for {} after {} attempts'.format(
                email,
                max_attempts
            )
        )

    def clean(self):
        email = self.cleaned_data.get('email')

        if email:
            self.cleaned_data['username'] = self.generate_username(email)

        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm, UniqueEmailFormMixin):
    email = forms.EmailField(required=True)


class CustomUserAdmin(UserAdmin):
    '''
    Simplified user admin for non-superusers, which also prevents such
    users from upgrading themselves to superuser.
    '''

    form = CustomUserChangeForm

    add_form_template = 'admin/add_user_form.html'

    add_form = CustomUserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',),
        }),
    )

    non_superuser_fieldsets = (
        (None, {'fields': (
            'username',
            # Even though we don't need/use the password field, showing it
            # is apparently required to make submitting changes work.
            'password'
        )}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(is_superuser=False)
        return qs

    def get_fieldsets(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return self.non_superuser_fieldsets
        return super().get_fieldsets(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
