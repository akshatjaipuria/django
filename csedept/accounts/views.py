from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from smtplib import SMTPException
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import time


# Create your views here.

def login(request):
    if request.method == 'POST':
        usn = request.POST['usn']
        password = request.POST['password']

        user = auth.authenticate(username=usn, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/home")
        else:
            messages.info(request, "Invalid Credentials!")
            return redirect("/")

    else:
        return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        usn = request.POST['usn']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username__iexact=usn).exists():
                messages.info(request, 'USN already registered!')
                return redirect('/register')
            elif User.objects.filter(email__iexact=email).exists():
                messages.info(request, 'E-mail ID already registered!')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=usn, password=password1, email=email, first_name=first_name,
                                                last_name=last_name)
                user.is_active = False
                user.save();

                current_site = get_current_site(request)
                email_subject = 'Activate Your Account'
                message = render_to_string('activate_account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email
                email = EmailMessage(email_subject, message, to=[to_email])
                try:
                    validate_email(to_email)
                    valid_email = True
                except ValidationError:
                    valid_email = False

                if valid_email:
                    email.send()
                    messages.info(request, 'Activation link has been sent!')
                else:
                    messages.info(request, 'Invalid Email address!')
                    return redirect('/register')

        else:
            messages.info(request, 'Password Mismatch!')
            return redirect('/register')

        return redirect('/')

    else:
        return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(request, 'Your account is active, login to continue.')
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')

