from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Plan,Line,Product,Transctions,WithdrawalRequest,Links,Payment

class WithdrawalInline(admin.TabularInline):
    model = CustomUser.withdrawalrequests.through
    extra = 1
class ProductInline(admin.TabularInline):
    model = CustomUser.products.through
    extra = 1

class TransctionsInline(admin.TabularInline):
    model = CustomUser.transctions.through
    extra = 1

class ReferInline(admin.TabularInline):
    model = CustomUser.referrals.through
    extra = 1
    fk_name = 'from_customuser'  # Ensure 'from_user' matches the field name in the Refer model

class LinksInline(admin.TabularInline):
    model = CustomUser.links.through
    extra = 1
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = [ProductInline,TransctionsInline,WithdrawalInline,ReferInline,LinksInline]
    list_display = ['email', 'first_name', 'last_name', 'mobile', 'is_active', 'is_staff', 'is_superuser', 'plan', 'payment_confirm']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'mobile')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Plan', {'fields': ('plan',)}),
        ('Profile Picture', {'fields': ('image',)}),
        ('Payment Confirmation', {'fields': ('payment_confirm',)}),
        ('Balance', {'fields': ('Balance',)}),
        ('Reward', {'fields': ('reward_earning',)}),
        ('TRX Documentation', {'fields': ('trx_id',)}),
        ('Invite Link', {'fields': ('invite_link',)}),
        ('Rank', {'fields': ('rank_level',)}),
        ('Show in Top Member', {'fields': ('on_dashboard',)}),
        ('Click on Link',{'fields':('click_on_link1','click_on_link2','click_on_link3','click_on_link4')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'mobile', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'plan'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'mobile')
    ordering = ('email',)

    # Remove references to groups and user_permissions
    filter_horizontal = ()
    list_filter = ()
    list_filter = ['withdrawalrequests__paid','payment_confirm',]
    def get_inline_instances(self, request, obj=None):
        if not obj:  # When adding a new CustomUser
            return list()
        return super().get_inline_instances(request, obj)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product)
admin.site.register(Transctions)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'request_date', 'account_name', 'account_number', 'billing_state', 'paid')
    list_filter = ('billing_state', 'paid')
    search_fields = ('email', 'account_name', 'account_number')
    readonly_fields = ('request_date',)  # Make request_date read-only in admin

admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)
class PlansAdmin(admin.ModelAdmin):
    list_display = ('id','plan_name', 'investment', 'daily_earning', 'products', 'per_product_earning', 'daily_earning_balance', 'image')
    search_fields = ['plan_name']
    list_filter = ['investment', 'daily_earning', 'products', 'per_product_earning', 'daily_earning_balance']
    list_per_page = 20

admin.site.register(Plan, PlansAdmin)


class LineAdmin(admin.ModelAdmin):
    list_display = ('text',)
class LinksAdmin(admin.ModelAdmin):
    list_display = ('url',)
admin.site.register(Line, LineAdmin)
admin.site.register(Links, LinksAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('number',)
admin.site.register(Payment, PaymentAdmin)
