from django.db import models

# Create your models here.
class Student(models.Model):
    std_name        =   models.CharField(max_length=50)
    std_mobile      =   models.CharField(max_length=10, unique=True)
    std_address     =   models.TextField()
    std_auth_type   =   models.CharField(
        choices=[
            ('ad', 'Aadhar Card'),
            ('ci', 'College ID'),
            ('vc', 'Voter Card'),
            ('dl', 'Driving License'),
        ],
        max_length=2)
    std_auth_id     =   models.CharField(max_length=100, unique=True)
    std_active      =   models.BooleanField(default=True)
    std_join_date   =   models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.std_name}'


class Staff(models.Model):
    stf_name        =   models.CharField(max_length=50)
    stf_mobile      =   models.CharField(max_length=10, unique=True)
    stf_address     =   models.TextField()
    stf_auth_type   =   models.CharField(
        choices=[
            ('ad', 'Aadhar Card'),
            ('ci', 'College ID'),
            ('vc', 'Voter Card'),
            ('dl', 'Driving License'),
        ],
        max_length=2)
    stf_auth_id     =   models.CharField(max_length=100, unique=True)
    stf_active      =   models.BooleanField(default=True)
    stf_join_date   =   models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.stf_name}'

