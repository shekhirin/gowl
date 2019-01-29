from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def user_signed_up_callback(request, user, **kwargs):
    gc = user.gc

    worksheet = gc.copy(file_id='1SOIQWiYGAAxKRPrSqQZSH7AA_OrNhjUW5g2Ib1FahnA', title='🏆 Gowl Spreadsheet',
                        copy_permissions=True)

    user.spreadsheetId = worksheet.id
    user.save()
