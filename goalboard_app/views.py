import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from oauth2client.client import AccessTokenCredentials
from allauth.socialaccount.models import SocialToken
import gspread

from goalboard_app.models import CustomUser
from goalboard_app.forms import ProfileForm
from goalboard_app.util import GoalboardSpreadsheet

from time import time


def home(request):
    raw_states = [request.user.is_authenticated,
                  hasattr(request.user, 'is_spreadsheet_set') and request.user.is_spreadsheet_set,
                  hasattr(request.user, 'is_username_set') and request.user.is_username_set]
    states = [''] * len(raw_states)
    for i, state in enumerate(raw_states):
        if state:
            states[i] = 'done'
        else:
            if i == 0 or raw_states[i - 1]:
                states[i] = 'active'
            else:
                states[i] = 'pending'
    return render(request, 'home.html', {'states': states})


def user_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user, initial={'username': request.user.username if request.user.is_username_set else None})
    if request.method == 'POST' and form.is_valid():
        request.user.is_username_set = True
        request.user.save()
        form.save()
        if 'continue' in request.GET:
            return HttpResponseRedirect(request.GET.get('continue'))
        else:
            return render(request, 'user_profile.html', {'form': form})

    return render(request, 'user_profile.html', {'form': form})


def user_goalboard(request, username):
    goalboard_user = CustomUser.objects.get(username=username)

    spreadsheet = GoalboardSpreadsheet(goalboard_user)

    return render(request, 'user_goalboard.html', {'goalboard_user': goalboard_user, 'spreadsheet': spreadsheet, 'avatar': goalboard_user.socialaccount_set.filter(provider='google')[0].extra_data['picture']})


def user_spreadsheet(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(home)

    if user.spreadsheetId:
        return HttpResponseRedirect(f'https://docs.google.com/spreadsheets/d/{user.spreadsheetId}')

    gc = user.gc

    worksheet = gc.copy(file_id='1SOIQWiYGAAxKRPrSqQZSH7AA_OrNhjUW5g2Ib1FahnA', title='🏆 Goalboard Spreadsheet',
                        copy_permissions=True)

    user.spreadsheetId = worksheet.id
    user.save()
    request.user = user

    return HttpResponseRedirect(f'https://docs.google.com/spreadsheets/d/{user.spreadsheetId}')
