from django.urls import path
from users import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('signup/',views.SignupView.as_view(),name='signup'),
    path('signup/complete/',views.Signup_CompleteView.as_view(),name='signup_complete'),
    path('region/',views.region_register_view,name='region'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('profile/edit/',views.ProfileEditView.as_view(),name='edit_profile'),
]