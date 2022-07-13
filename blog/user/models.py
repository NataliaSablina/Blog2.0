from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.safestring import mark_safe


def sex_control(sex):
    if sex == "male" or sex == "female":
        return True
    else:
        return False


class UserManager(BaseUserManager):

    def create_user(self, name, surname, email, phone_number, date_of_birth, sex, creation, photo, password=None):
        if not email:
            return ValueError("Users must have email.")
        if not sex_control(sex.lower()):
            sex = "Other"
        user = self.model(
            email=self.normalize_email(email),
        )
        user.name = name
        user.surname = surname
        user.phone_number = phone_number
        user.date_of_birth = date_of_birth
        user.sex = sex
        user.creation = creation
        user.photo = photo
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, surname, email, phone_number, date_of_birth, sex, creation, photo, password=None):
        user = self.create_user(
            name,
            surname,
            email,
            phone_number,
            date_of_birth,
            sex,
            creation,
            photo,
            password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=50, verbose_name="Name")
    surname = models.CharField(max_length=50, verbose_name="Surname")
    email = models.EmailField(unique=True, verbose_name="Email address")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'."
                                         " Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True,
                                    verbose_name="Phone Number")
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=50, verbose_name="Sex", blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Time of creation", blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True, verbose_name="Photo")
    is_active = models.BooleanField(default=True, verbose_name="Is active?")
    is_admin = models.BooleanField(default=False, verbose_name="Is admin?")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone_number', 'date_of_birth', 'sex']

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-creation_date']

    def __str__(self):
        return self.email

    def get_avatar(self):
        if not self.photo:
            return '/static/images/user_icon.png'
        return self.photo.url

    def avatar_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_avatar())

    avatar_tag.short_description = 'Avatar'

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # Simplest possible answer: All admins are staff
        return self.is_admin
