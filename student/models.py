from django.db import models

# Create your models here.
class Student(models.Model):
    std_name = models.CharField(max_length=50)
    std_mobile = models.CharField(max_length=10, unique=True)
    std_address = models.TextField()
    std_auth_id = models.CharField(max_length=100, unique=True)
    AUTH_TYPE = {
        'dl': 'Driving License',
        'ad': 'Aadhar Card',
        'vc': 'Voter Card',
        'ci': 'College ID'
    }
    std_auth_type = models.CharField(max_length=2, choices=AUTH_TYPE)
    std_active = models.BooleanField(default=True)
    join_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.std_name}:[{self.join_date}]"