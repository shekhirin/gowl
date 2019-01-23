from django import forms
from django.contrib.auth import get_user_model


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label='')

    class Meta:
       model = get_user_model()
       fields = ['username']

    def clean_username(self):
        username = self.cleaned_data['username']
        user_model = get_user_model()
        try:
            user_model.objects.exclude(id=self.instance.id).get(username__iexact=username)
        except user_model.DoesNotExist:
            return username
        raise forms.ValidationError("This username has already existed.")
