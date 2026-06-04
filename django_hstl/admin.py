from django.contrib import admin
from .models import (
	MyUser,
	Hostel,
	StudentProfile,
	StaffProfile,
	Room,
	Bed,
	Allocation,
	Invoice,
	Payment,
	StaffAttendance,
	Payroll,
	Complaint,
	LeaveRequest,
	Visitor
)
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Hostel)
admin.site.register(StudentProfile)
admin.site.register(StaffProfile)
admin.site.register(Room)
admin.site.register(Bed)
admin.site.register(Allocation)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(StaffAttendance)
admin.site.register(Payroll)
admin.site.register(Complaint)
admin.site.register(LeaveRequest)
admin.site.register(Visitor)