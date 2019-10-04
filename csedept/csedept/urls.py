"""csedept URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from materials import views as materials_views
from accounts import views as accounts_views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
                  re_path(r'^post/(.*)$', materials_views.post),
                  path('', accounts_views.login),
                  path('register/', accounts_views.register),
                  path('logout/', accounts_views.logout),
                  path('home/', materials_views.home),
                  path('admin/', admin.site.urls),
                  url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                      accounts_views.activate_account, name='activate'),
                  path('password/reset/', PasswordResetView.as_view(), name="password_reset"),
                  path('password/reset/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
                  path('password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
                       name="password_reset_confirm"),
                  path('password/done', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
                  path('accounts/login/', accounts_views.login),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)