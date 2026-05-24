from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from .forms import UserLogin, NewMember, MemberDetail, RoomDetail
from .models import MyUser, Room

# Custom view-level security decorators
def superuser_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_superuser,
        login_url='hstl:index',
        redirect_field_name=None
    )(view_func)

def staff_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_staff,
        login_url='hstl:index',
        redirect_field_name=None
    )(view_func)

def student_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_active and not u.is_staff and not u.is_superuser,
        login_url='hstl:index',
        redirect_field_name=None
    )(view_func)


def auth_response(request, content, key, val):
    user = authenticate(username=key, password=val)
    if user is not None and user.is_active:
        login(request, user)
        if request.user.is_superuser:
            return redirect('hstl:root_index')
        elif request.user.is_staff:
            return redirect('hstl:staff_index')
        else:
            return redirect('hstl:student_index')
    else:
        content['form'].add_error(None, "Login Error, Invalid Value(s)")
        return render(request, 'index.html', content)


def index(request):
    # If user is already authenticated, redirect them directly to their dashboard
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('hstl:root_index')
        elif request.user.is_staff:
            return redirect('hstl:staff_index')
        else:
            return redirect('hstl:student_index')

    content = {}
    if request.method == 'POST':
        content['form'] = UserLogin(request.POST)
        if content['form'].is_valid():
            return auth_response(
                request,
                content,
                content['form'].cleaned_data['key'],
                content['form'].cleaned_data['val']
            )
    else:
        content['form'] = UserLogin()
    return render(request, 'index.html', content)


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('hstl:index')


class RootR:
    @superuser_required
    def index(request):
        content = {
            'student': MyUser.objects.get_student(),
            'staff': MyUser.objects.get_staff(),
            'inactive': MyUser.objects.get_inactive(),
            'room': Room.objects.all(),
        }
        return render(request, 'root/index.html', content)

    @superuser_required
    def newStudent(request):
        content = {}
        if request.method == 'POST':
            content['form'] = NewMember(request.POST)
            if content['form'].is_valid():
                return redirect(
                    'hstl:info_student',
                    std_id=MyUser.objects.create_user(content['form'].cleaned_data)
                )
        else:
            content['form'] = NewMember()
        return render(request, 'root/newStudent.html', content)

    @superuser_required
    def newStaff(request):
        content = {}
        if request.method == 'POST':
            content['form'] = NewMember(request.POST)
            if content['form'].is_valid():
                return redirect(
                    'hstl:info_staff',
                    stf_id=MyUser.objects.create_user(content['form'].cleaned_data, True)
                )
        else:
            content['form'] = NewMember()
        return render(request, 'root/newStaff.html', content)

    @superuser_required
    def infoStudent(request, std_id):
        student = MyUser.objects.get_student(std_id)
        if student is None:
            return redirect('hstl:root_index')
        content = {'student': student}
        if request.method == 'POST':
            content['form'] = MemberDetail(request.POST, instance=student)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = MemberDetail(instance=student)
        return render(request, 'root/infoStudent.html', content)

    @superuser_required
    def infoStaff(request, stf_id):
        staff = MyUser.objects.get_staff(stf_id)
        if staff is None:
            return redirect('hstl:root_index')
        content = {'staff': staff}
        if request.method == 'POST':
            content['form'] = MemberDetail(request.POST, instance=staff)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = MemberDetail(instance=staff)
        return render(request, 'root/infoStaff.html', content)

    @superuser_required
    def newRoom(request):
        content = {}
        if request.method == 'POST':
            content['form'] = RoomDetail(request.POST)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = RoomDetail()
        return render(request, 'root/newRoom.html', content)

    @superuser_required
    def infoRoom(request, room_id):
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return redirect('hstl:root_index')
        content = {'room': room}
        if request.method == 'POST':
            content['form'] = RoomDetail(request.POST, instance=room)
            if content['form'].is_valid():
                content['form'].save()
                return redirect('hstl:root_index')
        else:
            content['form'] = RoomDetail(instance=room)
        return render(request, 'root/infoRoom.html', content)


class StudentR:
    @student_required
    def index(request):
        content = {'student': request.user}
        return render(request, 'student/index.html', content)


class StaffR:
    @staff_required
    def index(request):
        content = {'staff': request.user}
        return render(request, 'staff/index.html', content)

