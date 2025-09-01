from django.db import models
import uuid
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    referral_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    referred_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals')
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4()).replace('-', '')[:10]  # unique 10-char code
        super(Profile, self).save(*args, **kwargs)

    def _str_(self):
        return f"{self.user.username}'s profile"

    def referral_link(self):
        # Example: http://yourdomain.com/signup?ref=code
        return f"http://yourdomain.com/signup?ref={self.referral_code}"
    


class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class CashOutHistory(models.Model):
    user = models.ForeignKey(User, related_name='cash_outs', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])

    def __str__(self):
        return f"{self.amount} - {self.status} for {self.user.username} on {self.date}"



class Referral(models.Model):
    user = models.ForeignKey(User, related_name='referrals_user', on_delete=models.CASCADE,null = True, blank = True)
    referred_user = models.ForeignKey(User, related_name='referred_by', on_delete=models.CASCADE)
    date_referred = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Referral by {self.user.username} for {self.referred_user.username}"
    


class ReferralCashout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_cashouts',null = True, blank = True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - {self.amount}"



class InvestorAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="investor_account")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    account_status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('suspended', 'Suspended'),
            ('closed', 'Closed')
        ],
        default='active'
    )

    def _str_(self):
        return f"{self.user.username} - Balance: ${self.balance}"

    def withdraw(self, amount):
        """Handles withdrawal logic."""
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.save()

    def deposit(self, amount):
        """Handles deposit logic."""

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    minmum_deposit = models.DecimalField(max_digits=8, decimal_places=2)
    maxmum_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    return_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()

    def __str__(self) -> str:
        return self.name
    


class SubscribedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscriber_users")
    plan = models.OneToOneField(SubscriptionPlan, on_delete=models.CASCADE, related_name="subscribed_plan")
    activate = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True) # Get the date the user subscribed
    end_date = models.DateTimeField() # the date the user subscribed plus the duration

    def __str__(self):
        return f"{self.user} - {self.plan}"
    
class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    

    

class Deposit(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    CRYPTO_CHOICES = [
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending',null=True, blank=True)
    status = models.CharField(max_length=10, choices=(("pending","Pending"),("approved","Approved")), default="pending",null=True, blank=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    crypto = models.CharField(max_length=10, choices=CRYPTO_CHOICES, default="BTC",null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} - {self.amount} to {self.plan.name}"
    

class Payment(models.Model):
    investor_name = models.CharField(max_length=255)
    transaction_hash = models.CharField(max_length=64, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.investor_name} - {self.transaction_hash}"
    



class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    cryptocurrency = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    price_per_unit = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} {self.amount} {self.cryptocurrency} on {self.date}"
    


class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.CharField(max_length=50)
    invested_amount = models.DecimalField(max_digits=20, decimal_places=8)
    current_value = models.DecimalField(max_digits=20, decimal_places=2)
    investment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('closed', 'Closed')])

    def __str__(self):
        return f'{self.cryptocurrency} - {self.invested_amount}'
    




class Withdrawal(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.CharField(max_length=10, choices=CRYPTO_CHOICES, default="BTC",null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.status})"