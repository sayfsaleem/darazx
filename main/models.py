from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from django.core.validators import MaxValueValidator

class Plan(models.Model):
    plan_name = models.CharField(max_length=50)
    investment = models.PositiveIntegerField()
    daily_earning = models.PositiveIntegerField()
    products = models.PositiveIntegerField()
    per_product_earning = models.PositiveIntegerField()
    daily_earning_balance = models.PositiveIntegerField()
    link_earning = models.PositiveIntegerField(default=0)
    image = models.ImageField(null=False,blank=False)
    bonus = models.PositiveIntegerField(default=1)
    url = models.SlugField(default='')
    def __str__(self):
        return self.plan_name




class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, mobile, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, mobile=mobile)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, mobile, password=None):
        user = self.create_user(email, first_name, last_name, mobile, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
import io
from django.core.files.base import ContentFile


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(default='Unknown_person.jpg')
    Balance = models.IntegerField(default=0)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # You might want to use a more secure way to store passwords
    payment_confirm = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING, related_name='plans',null=True,blank=True)
    trx_id = models.TextField(max_length=505)
    invite_link = models.CharField(max_length=50, default=uuid.uuid4().hex)
    products = models.ManyToManyField('Product', related_name='products', blank=True)
    transctions = models.ManyToManyField('Transctions', related_name='transactions')
    withdrawalrequests = models.ManyToManyField('WithdrawalRequest', related_name='withdrawalrequests',)
    referrals = models.ManyToManyField('self', symmetrical=False, related_name='referrers')
    rank_level = models.IntegerField(default=1)
    on_dashboard = models.BooleanField(default=False)
    links = models.ManyToManyField('Links', blank=True, related_name="links")
    reward_earning = models.PositiveIntegerField(default=0)
    click_on_link1 = models.BooleanField(default=False)
    click_on_link2 = models.BooleanField(default=False)
    click_on_link3 = models.BooleanField(default=False)
    click_on_link4 = models.BooleanField(default=False)
    def update_rank(self):
        # Logic to update user's rank based on number of referrals
        referral_count = self.referrals.count()

        if referral_count >= 5:
            self.rank_level = 2
        elif referral_count >= 15:
            self.rank_level = 3
        elif referral_count >= 40:
            self.rank_level = 4
        elif referral_count >= 65:
            self.rank_level = 5
        elif referral_count >= 100:
            self.rank_level = 6
        elif referral_count >= 140:
            self.rank_level = 7
        elif referral_count >= 190:
            self.rank_level = 8
        elif referral_count >= 260:
            self.rank_level = 9
        elif referral_count >= 780:
            self.rank_level = 10
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class Line(models.Model):
    text = models.CharField(max_length=300)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(default='400.png')
    rating = models.IntegerField(validators=[MaxValueValidator(5)], default=1, null=False, blank=False, help_text='1 Means Minimum Rating, while 5 means Maximum Rating')
    def __str__(self):
        return self.name


class Transctions(models.Model):
    amount = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    trx = models.ImageField()
    def __str__(self):
        return str(self.date)


class WithdrawalRequest(models.Model):
    email = models.EmailField()
    topic = models.CharField(max_length=255,default="wallet")
    request_date = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date and time when an instance is created
    account_name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(default=0)
    account_number = models.CharField(max_length=16)
    billing_state = models.CharField(max_length=20, choices=[('EasyPaisa', 'EasyPaisa'), ('JazzCash', 'JazzCash')])
    paid = models.BooleanField(default=False)
    def __str__(self):
        return self.email


class Links(models.Model):
    name = models.CharField(max_length=90)
    url = models.URLField(max_length=1200)
    def __str__(self):
        return self.name

class Payment(models.Model):
    number = models.CharField(default="03270485632",max_length=15)
