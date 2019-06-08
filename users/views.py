import secrets

from datetime import timedelta
from django.http import HttpResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from users.models import User, Token


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


@csrf_exempt
def login(request):
    email = request.GET.get('email')
    password = request.GET.get('password')

    try:
        user = User.objects.get(email=email, password=password)
    except ObjectDoesNotExist:
        return HttpResponse('Wrong creds.')

    token = secrets.token_hex(32)
    Token.objects.create_token(token_value=token, user_id=user.id)
    return HttpResponse(f"{{token:{token}}}", content_type='application/json')


@csrf_exempt
def get_this_user(request):
    res = check_auth(request)
    if isinstance(res, HttpResponse):
        return res

    # Auth is fine already.
    token = request.GET.get('token', '')
    token = Token.objects.get(token_value=token)

    this_user = User.objects.get(id=token.user_id)
    data = serializers.serialize('json', [this_user])  # plural

    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_all_users(request):
    res = check_auth(request)
    if isinstance(res, HttpResponse):
        return res

    foos = User.objects.all()
    data = serializers.serialize('json', foos)

    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def logout(request):
    check_auth(request)

    return HttpResponse('', content_type='application/json')


def check_auth(request):
    # Auth
    token = request.GET.get('token', '')
    if token == '':
        return HttpResponse('no token')

    try:
        token = Token.objects.get(token_value=token)
    except ObjectDoesNotExist:
        return HttpResponse('Non authorized token.', status=403)

    # Check if token is obsolete
    elapsed = timezone.now() - token.last_update
    if elapsed > timedelta(hours=24):
        return HttpResponse('Obsolete token', status=403)

