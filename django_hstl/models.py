from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class MyManager(BaseUserManager):
    
    def create_superuser(self, mobile, password):
        try:
            user = self.model(
                mobile          =   int(mobile),
                auth_type       =   'a',
                is_superuser    =   True,
                name            =   input('Enter Name: '),
                address         =   input('Enter Address: '),
                auth_id         =   input('Enter Aadhar number: '),
            )
        except Exception as e:
            exit(f'Unable to create superuser...\n{e}')
        else:
            user.set_password(password)
            user.save()
        return f"SuperUser created."
    
    def create_student(self, data):
        try:
            user = self.model(
                name        =   data['name'],
                mobile      =   int(data['mobile']),
                address     =   data['address'],
                auth_type   =   data['auth_type'],
                auth_id     =   data['auth_id'],
            )
        except Exception as e:
            exit(f'Unable to create student...\n{e}')
        else:
            user.set_password(data['password'])
            user.save()
        return user.id
    
    def create_staff(self, data):
        try:
            user = self.model(
                name        =   data['name'],
                mobile      =   int(data['mobile']),
                address     =   data['address'],
                auth_type   =   data['auth_type'],
                auth_id     =   data['auth_id'],
                is_staff    =   True,
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
    name        =   models.CharField(max_length=50)
    mobile      =   models.CharField(max_length=10, unique=True)
    address     =   models.TextField()
    auth_type   =   models.CharField(
        choices=[
            ('a', 'Aadhar Card'),
            ('d', 'Driving License'),
        ],
        max_length=1
    )
    auth_id         =   models.CharField(max_length=12, unique=True)
    is_active       =   models.BooleanField(default=True)
    is_staff        =   models.BooleanField(default=False)
    is_superuser    =   models.BooleanField(default=False)
    join_date       =   models.DateField(auto_now_add=True)
    
    USERNAME_FIELD = 'mobile'
    
    objects     =   MyManager()
    
    def __str__(self):
        return f'{self.name}'


