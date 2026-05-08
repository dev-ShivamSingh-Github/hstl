from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .valids import (
    validate_mobile,
    validate_password,
    validate_name,
    validate_address,
    validate_aadhar
)

# Create your models here.


class MyManager(BaseUserManager):
    
    def create_superuser(self, **data):
        try:
            validate_password(data['password'])
            user = self.model(
                # auth_type       =   'a',
                name            =   data['name'],
                mobile          =   data['mobile'],
                address         =   data['address'],
                auth_id         =   data['auth_id'],
                is_staff        =   True,
                is_superuser    =   True
            )
        except Exception as e:
            exit(f'Unable to create superuser...\n{e}')
        else:
            user.set_password(data['password'])
            user.save()
        return f"SuperUser created."

    
    def create_user(self, data, staff=False):
        try:
            validate_password(data['password'])
            user = self.model(
                # auth_type   =   data['auth_type'],
                name        =   data['name'],
                mobile      =   data['mobile'],
                address     =   data['address'],
                auth_id     =   data['auth_id'],
                is_staff    =   staff,
            )
        except Exception as e:
            exit(f'Unable to create staff...\n{e}')
        else:
            user.set_password(data['password'])
            user.save()
        return user.id
    
    def get_student(self, id=None):
        if id is not None:
            try:
                return self.get(pk = id, is_staff = False, is_superuser = False)
            except Exception:
                return None
        return self.filter(is_staff = False, is_superuser = False, is_active = True)
    
    def get_staff(self, id=None):
        if id is not None:
            try:
                return self.get(pk = id, is_staff = True, is_superuser = False)
            except Exception:
                return None
        return self.filter(is_staff = True, is_superuser = False, is_active = True)


class MyUser(AbstractBaseUser):
    name = models.CharField(
        max_length=50,
        verbose_name='Name',
        help_text='Full Name of the user',
        validators=[validate_name]
    )
    mobile = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Mobile',
        help_text='Mobile number of the user',
        validators=[validate_mobile]
    )
    '''email = models.EmailField(
        verbose_name='Email',
        help_text='Email of the User'
    )
    auth_type = models.CharField(
        choices=[
            ('a', 'Aadhar Card'),
            ('d', 'Driving License'),
            ('c', 'College ID')
        ],
        max_length=1,
        verbose_name='ID type',
        help_text='Document Type of the user'
    )'''
    auth_id = models.CharField(
        max_length=12,
        unique=True,
        verbose_name='Aadhar',
        help_text='ID proof of the user',
        validators=[validate_aadhar]
    )
    address = models.TextField(
        max_length=200,
        verbose_name='Address',
        help_text='Address of the user',
        validators=[validate_address]
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Allow login?',
        help_text='Uncheck to delete the user'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Is Staff?',
        help_text='Uncheck to make the user a Student'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Is SuperUser?',
        help_text='Uncheck to make the user a Staff'
    )
    join_date = models.DateField(
        auto_now_add=True,
        verbose_name='Join Date',
        help_text='The date of joining of the User'
    )
    
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['name', 'auth_id', 'address']
    
    objects     =   MyManager()
    
    def __str__(self):
        return f'{self.name}'

