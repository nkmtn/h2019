from django.db import models, transaction

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class UserStatus(models.Model):
    user_status_code = models.IntegerField()
    user_status_name = models.CharField(max_length=255)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    user_password_salt = models.CharField(max_length=255, default=None)
    user_password_reset_token = models.CharField(max_length=255, default=None)
    user_password_reset_time = models.DateTimeField(default=None)
    user_invitation_token = models.CharField(max_length=255, default=None)
    user_invitation_time = models.DateTimeField(default=None)
    user_email_confirmation_token = models.CharField(max_length=255, default=None)
    user_phone = models.CharField(max_length=255, default=None)
    user_status_id = models.ForeignKey(UserStatus, on_delete=models.CASCADE, default=None)
    user_middle_name = models.CharField(max_length=255, default=None)
    user_birth_date = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)  # user_first_name
    last_name = models.CharField(max_length=30, blank=True)  # user_last_name
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)  # user_registration_time
    user_contact_json = models.TextField(default='')
    user_photo = models.TextField(default='')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


class TokenManager(models.Manager):
    def create_token(self, token_value, user_id):
        token = self.create(token_value=token_value, user_id=user_id)
        token.save()
        return token


class Token(models.Model):
    token_value = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)

    objects = TokenManager()


# class UserContact(models.Model):
#     user_contact_json = models.TextField()
#     user_contact_visible_to_users = models.SmallIntegerField()
#     user_contact_visible_to_others = models.SmallIntegerField()
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Worker(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_description = models.TextField()


class Employer(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    employer_position = models.CharField(max_length=255)


class Region(models.Model):
    region_name = models.CharField(max_length=255)
    region_code = models.IntegerField()


class Institution(models.Model):
    institution_name = models.CharField(max_length=255)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    parent_id = models.IntegerField()


class Supervisor(models.Model):
    is_moderator = models.SmallIntegerField()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    institution_id = models.ForeignKey(Institution, on_delete=models.CASCADE)


class Spec(models.Model):
    spec_code = models.IntegerField()
    spec_name = models.CharField(max_length=255)
    spec_level = models.IntegerField()


class Prof(models.Model):
    prof_title = models.CharField(max_length=255)
    prof_link = models.CharField(max_length=255)


class Spec2Prof(models.Model):
    spec_id = models.ForeignKey(Spec, on_delete=models.CASCADE)
    prof_id = models.ForeignKey(Prof, on_delete=models.CASCADE)


class EduPlan(models.Model):
    edu_acceptance_year = models.IntegerField()
    spec_id = models.ForeignKey(Spec, on_delete=models.CASCADE)
    institution_id = models.ForeignKey(Institution, on_delete=models.CASCADE)


class Education(models.Model):
    worker_id = models.ForeignKey(Worker, on_delete=models.CASCADE)
    edu_plan_id = models.ForeignKey(EduPlan, on_delete=models.CASCADE)
    start_year = models.IntegerField()
    finish_year = models.IntegerField()
    has_completed = models.SmallIntegerField()


class Position(models.Model):
    position_name = models.CharField(max_length=255)
    prof_id = models.ForeignKey(Prof, on_delete=models.CASCADE)


class Career(models.Model):
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    worker_id = models.ForeignKey(Worker, on_delete=models.CASCADE)


class Review(models.Model):
    career_id = models.ForeignKey(Career, on_delete=models.CASCADE)
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    text = models.TextField()


class Vacancy(models.Model):
    vacancy_name = models.CharField(max_length=255)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    position_idd = models.ForeignKey(Position, on_delete=models.CASCADE)


class Achieve(models.Model):
    worker_id = models.ForeignKey(Worker, on_delete=models.CASCADE)
    career_id = models.ForeignKey(Career, on_delete=models.CASCADE)
    published = models.DateTimeField()
    edited = models.DateTimeField()
    approved = models.DateTimeField()


class AchieveCategoryField(models.Model):
    achieve_category_field_name = models.CharField(max_length=255)
    achieve_category_field_order = models.IntegerField()
    achieve_category_field_type = models.IntegerField()  # string or int field


class AchieveCategory(models.Model):
    achieve_category_name = models.CharField(max_length=255)
    achieve_category_parent_id = models.ForeignKey('self', on_delete=models.CASCADE)


class AchieveFieldString(models.Model):
    achieve_id = models.ForeignKey(Achieve, on_delete=models.CASCADE)
    achieve_category_field_id = models.ForeignKey(AchieveCategoryField, on_delete=models.CASCADE)
    achieve_category_id = models.ForeignKey(AchieveCategory, on_delete=models.CASCADE)
    achieve_field_string_value = models.CharField(max_length=4096)


class AchieveFieldInt(models.Model):
    achieve_id = models.ForeignKey(Achieve, on_delete=models.CASCADE)
    achieve_category_field_id = models.ForeignKey(AchieveCategoryField, on_delete=models.CASCADE)
    achieve_category_id = models.ForeignKey(AchieveCategory, on_delete=models.CASCADE)
    achieve_field_value = models.IntegerField()
