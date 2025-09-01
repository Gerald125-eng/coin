from django.contrib import admin
from .models import (
    Profile, CashOutHistory, Referral, ReferralCashout, InvestorAccount,
    SubscriptionPlan, SubscribedUser, UserAccount, Deposit, Payment,
    Transaction, Investment, Withdrawal
)
from .models import ContactMessage
from django.core.mail import send_mail





class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

admin.site.register(ContactMessage, ContactMessageAdmin)



# ----------------------------
# Profile Admin
# ----------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'referral_code','referred_by')
    search_fields = ('user_username', 'useremail', 'referrer_username')


# ----------------------------
# CashOutHistory Admin
# ----------------------------
@admin.register(CashOutHistory)
class CashOutHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'status')
    search_fields = ('user_username', 'user_email')
    list_filter = ('status', 'date')


# ----------------------------
# Referral Admin
# ----------------------------
@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('user', 'referred_user', 'date_referred')
    search_fields = ('user_username', 'referred_user_username')
    list_filter = ('date_referred',)


# ----------------------------
# ReferralCashout Admin
# ----------------------------
@admin.register(ReferralCashout)
class ReferralCashoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)


# ----------------------------
# InvestorAccount Admin
# ----------------------------
@admin.register(InvestorAccount)
class InvestorAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'account_status', 'created_at', 'updated_at')
    search_fields = ('user_username', 'user_email')
    list_filter = ('account_status', 'created_at')


# ----------------------------
# SubscriptionPlan Admin
# ----------------------------
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'minmum_deposit', 'maxmum_deposit', 'return_rate', 'duration', 'created')
    search_fields = ('name',)
    list_filter = ('return_rate', 'created')


# ----------------------------
# SubscribedUser Admin
# ----------------------------
@admin.register(SubscribedUser)
class SubscribedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'activate', 'start_date', 'end_date')
    search_fields = ('user_username', 'plan_name')
    list_filter = ('activate', 'start_date')


# ----------------------------
# Deposit Admin
# ----------------------------
from django.utils import timezone
from .models import Deposit
from django.conf import settings

class DepositAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "amount", "status", "date", "approved_at")
    list_filter = ("status", "date")
    actions = ["approve_deposits"]

    def save_model(self, request, obj, form, change):
        old_status = None
        if obj.pk:
            old_status = Deposit.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if old_status != "approved" and obj.status == "approved":
            send_mail(
                "Deposit Approved",
                f"Dear {obj.user.username}, your deposit of ${obj.amount} into {obj.plan.name} has been approved!",
                settings.DEFAULT_FROM_EMAIL,
                [obj.user.email],
                fail_silently=False,
            )



admin.site.register(Deposit, DepositAdmin)

# ----------------------------
# Payment Admin
# ----------------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('investor_name', 'transaction_hash', 'amount', 'confirmed', 'created_at')
    search_fields = ('investor_name', 'transaction_hash')
    list_filter = ('confirmed', 'created_at')


# ----------------------------
# Transaction Admin
# ----------------------------
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'cryptocurrency', 'amount', 'price_per_unit', 'created_at')
    search_fields = ('user__username', 'cryptocurrency')
    list_filter = ('transaction_type', 'cryptocurrency', 'created_at')


# ----------------------------
# Investment Admin
# ----------------------------
@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'cryptocurrency', 'invested_amount', 'current_value', 'investment_date', 'status')
    search_fields = ('user__username', 'cryptocurrency')
    list_filter = ('status', 'investment_date')


# ----------------------------
# Withdrawal Admin
# ----------------------------
from .models import Withdrawal
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'crypto', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('status', 'crypto', 'created_at')


    def save_model(self, request, obj, form, change):
        old_status = None
        if obj.pk:
            old_status = Withdrawal.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if old_status != "approved" and obj.status == "approved":
            send_mail(
                "Withdrawal Approved",
                f"Dear {obj.user.username}, your withdrawal of ${obj.amount} has been approved and processed.",
                settings.DEFAULT_FROM_EMAIL,
                [obj.user.email],
                fail_silently=False,
            )


admin.site.register(Withdrawal, WithdrawalAdmin)

