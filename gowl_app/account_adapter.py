from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from gowl import settings


class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False

    def get_login_redirect_url(self, request):
        if request.LANGUAGE_CODE == settings.LANGUAGE_CODE:
            return '/#gettingstarted'
        else:
            return f'/{request.LANGUAGE_CODE}/#gettingstarted'


class NoNewUsersSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return True