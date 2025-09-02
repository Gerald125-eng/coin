


from django.urls import path
from . import views

urlpatterns = [
      path("", views.index, name="index"),
    path('contact/', views.contact_view, name='contact'),
    path('account_security/', views.account_security, name='account_security'),
    path('about_us/', views.about_us, name='about_us'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("confirm_deposit/confirm_deposit/", views.confirm_deposit, name="confirm_deposit"),
    path("plan/<int:pk>/", views.plan_detail, name="plan_detail"),
    path("plan/<int:pk>/deposit/", views.make_deposit, name="make_deposit"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("my_referal/", views.my_referal, name="my_referal"),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('request-withdrawal/', views.request_withdrawal, name='request_withdrawal')
]