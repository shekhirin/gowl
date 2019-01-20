import gspread
from allauth.socialaccount.models import SocialToken
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse
from oauth2client.client import AccessTokenCredentials

from datetime import datetime, timezone, timedelta
import requests


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    spreadsheetId = models.CharField(max_length=100, blank=True)
    is_username_set = models.BooleanField(default=False)
    is_spreadsheet_set = models.BooleanField(default=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def google_token(self):
        token = SocialToken.objects.get(account__user=self, account__provider='google')
        if token.expires_at > datetime.now(timezone.utc):
            return token

        r = requests.post('https://www.googleapis.com/oauth2/v4/token', data={
            'client_id': token.app.client_id,
            'client_secret': token.app.secret,
            'refresh_token': token.token_secret,
            'grant_type': 'refresh_token'
        }).json()

        token.token = r['access_token']
        token.expires_at = datetime.now(timezone.utc) + timedelta(seconds=r['expires_in'])
        token.save()

        return token

    @property
    def gc(self):
        credentials = AccessTokenCredentials(self.google_token, 'goalboard/1.0')
        gc = gspread.authorize(credentials)

        return gc

    @property
    def goalboard_url(self):
        return reverse('user_goalboard', kwargs={'username': self.username})
