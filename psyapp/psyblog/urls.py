from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog.views.home, name='home'),
    path('login/', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('psychologue/inscription/', authentication.views.psychologue_registration_view, name='psychologue_registration'),
    path('patient/inscription/', authentication.views.patient_registration_view, name='patient_registration'),
    path('text/create/', blog.views.TextCreateView.as_view(), name='create_text'),
    path('register_patient/', authentication.views.register_patient, name='register_patient'),
    path('emotions_patient',blog.views.emotions_patient,name='emotions_patient'),
    path('recherche_textes/', blog.views.recherche_textes, name="recherche_textes"),
    path('emotions_dashboard/', blog.views.emotions_dashboard, name='emotions_dashboard'),
]

