from django.urls import path
from . import views
urlpatterns = [
path ('Signup/',views.SignUp.as_view()),  
path('login/',views.Login.as_view()),
path('user/',views.UserView.as_view()),
path('logout/',views.LogOut.as_view()),
path('resetpassword/',views.ResetPassword.as_view()),
path('passwordResetcheck/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='passwordReset-confirm'),
path('passwordResetComplete/',views.SetNewPasswordAPI.as_view(),name='passwordResetComplete'),
]