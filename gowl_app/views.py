import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from oauth2client.client import AccessTokenCredentials
from allauth.socialaccount.models import SocialToken
import gspread

from gowl_app.models import CustomUser
from gowl_app.forms import ProfileForm
from gowl_app.util import GowlSpreadsheet

from time import time
import datetime


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
        if 'next' in request.GET:
            return redirect(request.GET.get('next'))
        else:
            return render(request, 'user_profile.html', {'form': form})

    return render(request, 'user_profile.html', {'form': form})


def user_gowl(request, username):
    try:
        gowl_user = CustomUser.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect('home')

    try:
        spreadsheet = GowlSpreadsheet(gowl_user)
    except ObjectDoesNotExist:
        return redirect('home')

    return render(
        request, 
        'user_gowl.html', 
        {
            'gowl_user': gowl_user, 
            'spreadsheet': spreadsheet, 
            'avatar': gowl_user.socialaccount_set.filter(provider='google')[0].extra_data['picture'],
            'year': datetime.datetime.now().year
        }
    )


def user_spreadsheet(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('home')

    if not user.is_spreadsheet_set:
        user.is_spreadsheet_set = True
        user.save()

    if user.spreadsheetId:
        return redirect(f'https://docs.google.com/spreadsheets/d/{user.spreadsheetId}')

    gc = user.gc

    worksheet = gc.copy(file_id='1SOIQWiYGAAxKRPrSqQZSH7AA_OrNhjUW5g2Ib1FahnA', title='🏆 Gowl Spreadsheet',
                        copy_permissions=False)

    user.spreadsheetId = worksheet.id
    user.save()
    request.user = user

    return redirect(f'https://docs.google.com/spreadsheets/d/{user.spreadsheetId}')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')