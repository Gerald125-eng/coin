from django.shortcuts import render
# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from .models import  Deposit, Withdrawal,SubscriptionPlan,Profile
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from .models import Referral
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import UpdateUserForm, UpdatePasswordForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ContactMessage
from decimal import Decimal, InvalidOperation





def register_view(request):
    referral_code = request.GET.get('ref', None)  # ?ref=REFCODE in URL

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            if referral_code:
                try:
                    referrer = Profile.objects.get(referral_code=referral_code).user
                    user.profile.referred_by = referrer
                    user.profile.save()
                except Profile.DoesNotExist:
                    pass  # invalid referral code
                
            send_mail(
                    "Welcome to CryptoSite!",
                    f"Hello {user.username},\n\nWelcome to our company! We are happy to have you onboard.",
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True,
            )
                
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')

    return render(request, 'register.html', {'referral_code': referral_code})



# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')



# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

# Home view (requires login)
@login_required
def home_view(request):
    return render(request, 'home.html')



def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        # Validation
        if not name or not email or not subject or not message_text:
            messages.error(request, "All fields are required.")
        else:
            contact_message = ContactMessage(
                name=name,
                email=email,
                subject=subject,
                message=message_text
            )
            if request.user.is_authenticated:
                contact_message.user = request.user
            contact_message.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')

    return render(request, 'contact.html')



def index(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, "index.html", {"plans": plans})



def about_us(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, "about_us.html", {"plans": plans})




def plan_detail(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)
    return render(request, "plan_detail.html", {"plan": plan})





def make_deposit(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)

    if request.method == "POST":
        amount_str = request.POST.get("amount")

        if not amount_str:
            return render(request, "plan_detail.html", {"plan": plan, "error": "Amount is required."})

        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            return render(request, "plan_detail.html", {"plan": plan, "error": "Enter a valid deposit amount."})

        # Create deposit as pending
        deposit = Deposit.objects.create(
            user=request.user,
            plan=plan,
            amount=amount,
            status="pending",
        )

        # Email user
        send_mail(
            "Deposit Submitted",
            f"Dear {request.user.username}, you submitted a deposit of ${amount} into {plan.name}. Pending admin approval.",
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )

        # Email admin
        send_mail(
            "New Deposit Request",
            f"{request.user.username} requested a deposit of ${amount} into {plan.name}.",
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_NOTIFY_EMAIL],
            fail_silently=False,
        )

        return redirect("confirm_deposit")

    return render(request, "plan_detail.html", {"plan": plan})







@login_required
def request_withdrawal(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount:
            withdrawal = Withdrawal.objects.create(user=request.user, amount=amount)

            # Email user
            send_mail(
                "Withdrawal Request Submitted",
                f"Dear {request.user.username}, you requested a withdrawal of ${amount}. Pending admin approval.",
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )

            # Email admin
            send_mail(
                "New Withdrawal Request",
                f"{request.user.username} requested a withdrawal of ${amount}.",
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_NOTIFY_EMAIL],
                fail_silently=True,
            )
            return redirect("dashboard")
    return render(request, "request_withdrawal.html")





from django.db.models import Sum

def dashboard(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    referrals = user.referrals.all()  # users referred by this user
    referral_link = request.build_absolute_uri(f"/register/?ref={user.profile.referral_code}")

    # Only approved deposits and withdrawals
    deposits = Deposit.objects.filter(user=user, status="approved")
    withdrawals = Withdrawal.objects.filter(user=user, status="approved")  # Assuming you have status field

    total_deposit = deposits.aggregate(Sum("amount"))["amount__sum"] or 0
    total_withdrawal = withdrawals.aggregate(Sum("amount"))["amount__sum"] or 0
    last_deposit = deposits.order_by("-date").first()
    last_withdrawal = withdrawals.order_by("-created_at").first()
    balance = total_deposit - total_withdrawal

    # Also pass all deposits (approved + pending) if you want to show pending deposits separately
    all_deposits = Deposit.objects.filter(user=user)

    context = {
        'user': user,
        'profile': profile,
        "total_deposit": total_deposit,
        "total_withdrawal": total_withdrawal,
        "last_deposit": last_deposit,
        "last_withdrawal": last_withdrawal,
        "balance": balance,
        "deposits": all_deposits,  # includes pending
        "withdrawals": withdrawals,
        'referrals': referrals, 
        'referral_link': referral_link
    }
    return render(request, "dashboard.html", context)



def my_referal(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    referrals = user.referrals.all()  # users referred by this user
    referral_link = request.build_absolute_uri(f"/register/?ref={user.profile.referral_code}")

    context = {
        'referrals': referrals, 
        'referral_link': referral_link
    }
    return render(request, "my_referal.html", context)



def confirm_deposit(request,):
    
    if request.method == "POST":
        amount = request.POST.get("amount")
        tx_hash = request.POST.get("transaction_hash")

       

            # Send confirmation email
        send_mail(
                "Deposit Submitted",
                f"Dear {request.user.username}, you submitted a deposit of ${amount} into {SubscriptionPlan.name}.\n"
                f"Transaction Hash: {tx_hash}\nPending admin approval.",
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )

            # Notify admin
            # send_mail(
            #     "New Deposit Request",
            #     f"{request.user.username} deposited ${amount} into {plan.name}. Transaction hash: {tx_hash}",
            #     settings.DEFAULT_FROM_EMAIL,
            #     [settings.ADMIN_NOTIFY_EMAIL],
            #     fail_silently=True,
            # )

        return redirect("dashboard")

    return render(request, "confirm_deposit.html", )







@login_required
def update_profile(request):
    user = request.user
    # Add your profile update logic here
    return render(request, 'update_profile.html', {'user': user})


@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        password_form = UpdatePasswordForm(user, request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')  # Or wherever you want
            # Send confirmation email

        send_mail(
                'Profile Updated',
                f'Hello {user.username}, your username and password have been updated successfully.',
                'your-email@gmail.com',  # From
                [user.email],            # To
                fail_silently=False,
            )
    else:
        user_form = UpdateUserForm(instance=user)
        password_form = UpdatePasswordForm(user)
    
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })



def referral_list(request):
    referrals = Referral.objects.select_related("referrer").all().order_by("-created_at")
    return render(request, "referrals.html", {"referrals": referrals})