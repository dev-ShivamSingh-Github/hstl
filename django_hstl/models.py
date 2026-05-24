from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .valids import (
    validate_mobile,
    validate_password,
    validate_name,
    validate_address,
    validate_aadhar,
    validate_price
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

    def get_inactive(self, id=None):
        if id is not None:
            pass
        return self.filter(is_active = False).order_by('-is_staff') # True first because is 1


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

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    room_number = models.CharField(
        max_length=5,
        unique=True,
        verbose_name='Room Number',
        help_text='Eg.AS101:A=AC,S=Single',
    )
    room_type = models.CharField(
        max_length=2,
        choices=[
            ('A1', 'AC Single'),
            ('N1', 'Non-AC Single'),
            ('A2', 'AC Double'),
            ('N2', 'Non-AC Double'),
            ('A3', 'AC Triple'),
            ('N3', 'Non-AC Triple'),
            ('A4', 'AC Quadruple'),
            ('N4', 'Non-AC Quadruple'),
        ],
        verbose_name='Room Type',
        help_text='Select a room type'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price',
        help_text='Price of the Room',
        validators=[validate_price]
    )
    def __str__(self):
        return f"Room"


class Bed(models.Model):
    myuser = models.OneToOneField(
        MyUser,
        on_delete=models.SET_NULL,
        limit_choices_to={
            'is_staff': False,
            'is_superuser': False,
            'is_active': True
        },
        blank=True,
        null = True,
        verbose_name='StudentID',
        help_text='...'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name='RoomID',
        help_text='...'
    )
    def __str__(self):
        return f"Bed is occupied"


class Fee(models.Model):
    bed = models.ForeignKey(
        Bed,
        on_delete=models.CASCADE,
        verbose_name='BedID',
        help_text='...'
    )
    status = models.CharField(
        max_length=1,
        choices=[
            ('P', 'Paid'),
            ('U', 'Pending'),
            ('O', 'Overdue'),
        ],
        default='U',
        verbose_name='Payment Status',
        help_text='Status of the payment'
    )
    paid_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Payment Date',
        help_text='Date of the payment'
    )
    '''amount_due = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Amount Due',
        help_text='Due amount of the student'
    )
    due_date = models.DateField(
        default=bed.myuser.join_date,
        verbose_name='Due Date',
        help_text='Payment day of the student'
    )'''

    def __str__(self):
        return f"Invoice"


class Complaint(models.Model):
    bed = models.ForeignKey(
        Bed,
        on_delete=models.CASCADE,
        verbose_name='BedID',
        help_text='...'
    )
    category = models.CharField(
        max_length=1,
        choices=[
            ('E', 'Electrical'),
            ('P', 'Plumbing'),
            ('C', 'Cleaning'),
            ('I', 'Internet'),
            ('O', 'Other'),
        ],
        verbose_name='Category',
        help_text='Category of the Complaint'
    )
    status = models.CharField(
        max_length=1,
        choices=[
            ('O', 'Open'),
            ('R', 'Resolved'),
            ('I', 'In Progress'),
        ],
        default='O',
        verbose_name='Status',
        help_text='Status of Complaint'
    )
    description = models.TextField(
        max_length=500,
        verbose_name='Description',
        help_text='Please tell us more about issue'
    )
    raised_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Raised on',
        help_text='Ticket raised on'
    )
    # Added so the Admin can leave a note (e.g., "Electrician called, will visit tomorrow")
    admin_remarks = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        verbose_name='Admin Rmarks',
        help_text='Admin remark on Complaint'
    )
    
    def __str__(self):
        return f"Complaint"

