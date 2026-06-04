from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from .valids import (
    validate_mobile,
    validate_password,
    validate_name,
    validate_address,
    validate_aadhar,
    validate_price
)


class MyManager(BaseUserManager):
    
    def create_superuser(self, **data):
        try:
            validate_password(data.get('password', ''))
            user = self.model(
                name = data.get('name', 'Admin'),
                mobile = data['mobile'],
                is_staff = True,
                is_superuser = True
            )
        except Exception as e:
            raise ValidationError(f'Unable to create superuser: {e}')
        else:
            user.set_password(data['password'])
            user.save(using=self._db)
        return user

    def create_user(self, data, staff=False):
        try:
            validate_password(data['password'])
            user = self.model(
                name = data['name'],
                mobile = data['mobile'],
                is_staff = staff,
            )
        except Exception as e:
            raise ValidationError(f'Unable to create user: {e}')
        else:
            user.set_password(data['password'])
            user.save(using=self._db)
        return user.id
    
    def get_student(self, id=None):
        if id is not None:
            try:
                return self.get(pk=id, is_staff=False, is_superuser=False)
            except Exception:
                return None
        return self.filter(is_staff=False, is_superuser=False, is_active=True)
    
    def get_staff(self, id=None):
        if id is not None:
            try:
                return self.get(pk=id, is_staff=True, is_superuser=False)
            except Exception:
                return None
        return self.filter(is_staff=True, is_superuser=False, is_active=True)

    def get_inactive(self, id=None):
        return self.filter(is_active=False).order_by('-is_staff')


class MyUser(AbstractBaseUser, PermissionsMixin):
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
    is_active = models.BooleanField(
        default=True,
        verbose_name='Allow login?',
        help_text='Uncheck to disable the user'
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
    REQUIRED_FIELDS = ['name']
    
    objects = MyManager()

    def __str__(self):
        role = "Admin" if self.is_superuser else ("Staff" if self.is_staff else "Student")
        return f'{self.name} ({role})'

class Hostel(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Hostel Name',
        help_text='Name of the hostel'
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Hostel Code',
        help_text='Short code for the hostel (e.g., BH1)'
    )
    gender_type = models.CharField(
        max_length=1,
        choices=[('M', 'Boys'),('F', 'Girls'),('C', 'Co-ed'),],
        verbose_name='Gender Type',
        help_text='Allowed gender for this hostel'
    )
    chief_warden = models.ForeignKey(
        MyUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_hostels',
        limit_choices_to={'is_staff': True},
        verbose_name='Chief Warden',
        help_text='Staff member managing this hostel'
    )
    capacity = models.PositiveIntegerField(
        default=0,
        verbose_name='Capacity',
        help_text='Total student capacity of the hostel'
    )

    def __str__(self):
        return f"{self.name} ({self.get_gender_type_display()})"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='User',
        help_text='Associated user account'
    )
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Male'),('F', 'Female'),('O', 'Other'),],
        verbose_name='Gender',
        help_text='Gender of the student'
    )
    parent_name = models.CharField(
        max_length=100,
        verbose_name='Parent Name',
        help_text='Name of the parent or guardian',
        validators=[validate_name]
    )
    parent_mobile = models.CharField(
        max_length=10,
        verbose_name='Parent Mobile',
        help_text='Mobile number of the parent or guardian',
        validators=[validate_mobile]
    )
    blood_group = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        verbose_name='Blood Group',
        help_text='Blood group of the student'
    )
    address = models.TextField(
        verbose_name='Address',
        help_text='Permanent address of the student',
        validators=[validate_address]
    )
    course = models.CharField(
        max_length=100,
        verbose_name='Course',
        help_text='Course or program the student is enrolled in'
    )
    auth_id = models.CharField(
        max_length=12,
        unique=True,
        verbose_name='Aadhar',
        help_text='ID proof of the user',
        validators=[validate_aadhar]
    )

    def __str__(self):
        return f"Profile - {self.user.name}"


class StaffProfile(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        verbose_name='User',
        help_text='Associated user account'
    )
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Male'),('F', 'Female'),('O', 'Other'),],
        verbose_name='Gender',
        help_text='Gender of the staff member'
    )
    designation = models.CharField(
        max_length=100,
        verbose_name='Designation',
        help_text='Job title or designation of the staff member'
    )
    hostel_assigned = models.ForeignKey(
        Hostel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Hostel Assigned',
        help_text='Hostel assigned to this staff member'
    )
    shift = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Shift',
        help_text='Working shift of the staff member'
    )
    base_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Base Salary',
        help_text='Base monthly salary'
    )
    hire_date = models.DateField(
        auto_now_add=True,
        verbose_name='Hire Date',
        help_text='Date when the staff member was hired'
    )
    auth_id = models.CharField(
        max_length=12,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Aadhar',
        help_text='ID proof of the staff member',
        validators=[validate_aadhar]
    )

    def __str__(self):
        return f"{self.designation} - {self.user.name}"


class Room(models.Model):
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name='Hostel',
        help_text='Hostel this room belongs to'
    )
    room_number = models.CharField(
        max_length=10,
        verbose_name='Room Number',
        help_text='Unique number or identifier for the room'
    )
    room_type = models.CharField(
        max_length=2,
        choices=[
            ('A1', 'AC Single'), ('N1', 'Non-AC Single'),
            ('A2', 'AC Double'), ('N2', 'Non-AC Double'),
            ('A3', 'AC Triple'), ('N3', 'Non-AC Triple'),
            ('A4', 'AC Quadruple'), ('N4', 'Non-AC Quadruple'),
        ],
        verbose_name='Room Type',
        help_text='Type and capacity of the room'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price',
        help_text='Price of the room',
        validators=[validate_price]
    )

    class Meta:
        unique_together = ('hostel', 'room_number')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            num_beds = int(self.room_type[1])
            for _ in range(num_beds):
                Bed.objects.create(room=self)

    def __str__(self):
        return f"{self.hostel.code} - Room {self.room_number}"


class Bed(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='beds',
        verbose_name='Room',
        help_text='Room this bed is located in'
    )
    status = models.CharField(
        max_length=1,
        choices=[('A', 'Available'),('O', 'Occupied'),('M', 'Maintenance'),],
        default='A',
        verbose_name='Status',
        help_text='Current status of the bed'
    )

    def __str__(self):
        return f"{self.room.room_number} - Bed {self.id}"


class Allocation(models.Model):
    student = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': False},
        verbose_name='Student',
        help_text='Student allocated to this bed'
    )
    bed = models.ForeignKey(
        Bed,
        on_delete=models.CASCADE,
        verbose_name='Bed',
        help_text='Bed allocated to the student'
    )
    start_date = models.DateField(
        verbose_name='Start Date',
        help_text='Date when the allocation begins'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='End Date',
        help_text='Date when the allocation ends'
    )
    status = models.CharField(
        max_length=1,
        choices=[('A', 'Active'), ('C', 'Completed'), ('X', 'Cancelled')],
        default='A',
        verbose_name='Status',
        help_text='Current status of the allocation'
    )

    def clean(self):
        super().clean()
        if hasattr(self, 'student') and hasattr(self, 'bed'):
            try:
                student_gender = self.student.student_profile.gender
                hostel_gender = self.bed.room.hostel.gender_type
                if hostel_gender != 'C': # If not Co-ed
                    if student_gender != hostel_gender:
                        raise ValidationError("Student gender does not match Hostel gender type.")
            except StudentProfile.DoesNotExist:
                raise ValidationError("Student profile does not exist.")

    def __str__(self):
        return f"{self.student.name} -> {self.bed.room.room_number} ({self.get_status_display()})"


class Invoice(models.Model):
    student = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': False},
        verbose_name='Student',
        help_text='Student this invoice belongs to'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Title',
        help_text='Title or description of the invoice'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Amount',
        help_text='Total amount due for the invoice'
    )
    due_date = models.DateField(
        verbose_name='Due Date',
        help_text='Date by which the invoice must be paid'
    )
    status = models.CharField(
        max_length=1,
        choices=[('U', 'Unpaid'), ('P', 'Partially Paid'), ('F', 'Fully Paid')],
        default='U',
        verbose_name='Status',
        help_text='Payment status of the invoice'
    )

    def __str__(self):
        return f"Invoice #{self.id} - {self.student.name} ({self.get_status_display()})"


class Payment(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Invoice',
        help_text='Invoice this payment is applied to'
    )
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Amount Paid',
        help_text='Amount paid in this transaction'
    )
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Transaction ID',
        help_text='Unique identifier for the payment transaction'
    )
    paid_on = models.DateField(
        auto_now_add=True,
        verbose_name='Paid On',
        help_text='Date when the payment was made'
    )
    received_by = models.ForeignKey(
        MyUser,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'is_staff': True},
        verbose_name='Received By',
        help_text='Staff member who received the payment'
    )

    def __str__(self):
        return f"Payment {self.transaction_id} for Invoice #{self.invoice.id}"


class StaffAttendance(models.Model):
    staff = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True},
        verbose_name='Staff Member',
        help_text='Staff member this attendance record belongs to'
    )
    date = models.DateField(
        verbose_name='Date',
        help_text='Date of the attendance record'
    )
    status = models.CharField(
        max_length=2,
        choices=[('P', 'Present'), ('A', 'Absent'), ('HD', 'Half-Day'), ('L', 'On Leave')],
        verbose_name='Status',
        help_text='Attendance status for the date'
    )
    time_in = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Time In',
        help_text='Time the staff member checked in'
    )
    time_out = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Time Out',
        help_text='Time the staff member checked out'
    )

    class Meta:
        unique_together = ('staff', 'date')

    def __str__(self):
        return f"{self.staff.name} - {self.date} ({self.get_status_display()})"


class Payroll(models.Model):
    staff = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True},
        verbose_name='Staff Member',
        help_text='Staff member this payroll record belongs to'
    )
    month_year = models.DateField(
        verbose_name='Month/Year',
        help_text='Use the 1st of the month to represent the pay period'
    )
    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Basic Salary',
        help_text='Basic salary for the pay period'
    )
    deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Deductions',
        help_text='Total deductions for the pay period'
    )
    net_payable = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Net Payable',
        help_text='Net amount payable after deductions'
    )
    status = models.CharField(
        max_length=1,
        choices=[('P', 'Pending'), ('D', 'Paid')],
        default='P',
        verbose_name='Status',
        help_text='Payment status of the payroll record'
    )
    paid_on = models.DateField(
        null=True,
        blank=True,
        verbose_name='Paid On',
        help_text='Date when the payroll was paid'
    )

    class Meta:
        unique_together = ('staff', 'month_year')

    def __str__(self):
        return f"Payroll {self.staff.name} - {self.month_year.strftime('%B %Y')}"


class Complaint(models.Model):
    student = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='complaints',
        verbose_name='Student',
        help_text='Student who raised the complaint'
    )
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        verbose_name='Hostel',
        help_text='Hostel where the issue occurred'
    )
    category = models.CharField(
        max_length=1,
        choices=[('E', 'Electrical'), ('P', 'Plumbing'), ('C', 'Cleaning'), ('I', 'Internet'), ('O', 'Other')],
        verbose_name='Category',
        help_text='Category of the complaint'
    )
    description = models.TextField(
        verbose_name='Description',
        help_text='Detailed description of the issue'
    )
    status = models.CharField(
        max_length=1,
        choices=[('O', 'Open'), ('I', 'In Progress'), ('R', 'Resolved')],
        default='O',
        verbose_name='Status',
        help_text='Current status of the complaint'
    )
    assigned_to = models.ForeignKey(
        MyUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints',
        limit_choices_to={'is_staff': True},
        verbose_name='Assigned To',
        help_text='Staff member assigned to resolve the complaint'
    )
    raised_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Raised On',
        help_text='Date and time the complaint was raised'
    )
    admin_remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name='Admin Remarks',
        help_text='Remarks or notes from the administration'
    )

    def __str__(self):
        return f"Complaint #{self.id} ({self.get_category_display()}) - {self.hostel.code}"


class LeaveRequest(models.Model):
    student = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': False},
        verbose_name='Student',
        help_text='Student requesting the leave'
    )
    departure_date = models.DateTimeField(
        verbose_name='Departure Date',
        help_text='Date and time of departure'
    )
    return_date = models.DateTimeField(
        verbose_name='Return Date',
        help_text='Expected date and time of return'
    )
    reason = models.TextField(
        verbose_name='Reason',
        help_text='Reason for the leave request'
    )
    status = models.CharField(
        max_length=1,
        choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')],
        default='P',
        verbose_name='Status',
        help_text='Current status of the leave request'
    )
    approved_by = models.ForeignKey(
        MyUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves',
        limit_choices_to={'is_staff': True},
        verbose_name='Approved By',
        help_text='Staff member who approved the leave'
    )

    def __str__(self):
        return f"Leave {self.student.name} ({self.get_status_display()})"


class Visitor(models.Model):
    student = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        verbose_name='Student',
        help_text='Student the visitor is meeting'
    )
    visitor_name = models.CharField(
        max_length=100,
        verbose_name='Visitor Name',
        help_text='Name of the visitor'
    )
    relation = models.CharField(
        max_length=50,
        verbose_name='Relation',
        help_text='Relationship of the visitor to the student'
    )
    check_in = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Check-In Time',
        help_text='Date and time the visitor checked in'
    )
    check_out = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Check-Out Time',
        help_text='Date and time the visitor checked out'
    )
    logged_by = models.ForeignKey(
        MyUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='logged_visitors',
        limit_choices_to={'is_staff': True},
        verbose_name='Logged By',
        help_text='Staff member who logged the visitor entry'
    )

    def __str__(self):
        return f"Visitor: {self.visitor_name} for {self.student.name}"

