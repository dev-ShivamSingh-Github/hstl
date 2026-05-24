from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django_hstl.models import Room, Bed

User = get_user_model()

class RoomManagementTests(TestCase):
    def setUp(self):
        # Create a superuser
        # The MyManager.create_superuser creates the user and saves it.
        # It takes name, mobile, address, auth_id, password.
        # Let's check how MyManager.create_superuser expects kwargs.
        # Yes, name, mobile, address, auth_id, password.
        self.superuser = User.objects.model(
            name="Super User",
            mobile="9876543210",
            address="Admin Quarter",
            auth_id="123456789012",
            is_staff=True,
            is_superuser=True
        )
        self.superuser.set_password("Password@123")
        self.superuser.save()

        # Create a student user
        self.student = User.objects.model(
            name="John Doe",
            mobile="9111111111",
            address="Student Room 1",
            auth_id="111122223333",
            is_staff=False,
            is_superuser=False
        )
        self.student.set_password("Password@123")
        self.student.save()

    def test_bed_autocreation_on_room_creation(self):
        # Create N3 room, should create 3 beds
        room1 = Room.objects.create(room_number="N3-01", room_type="N3", price="1500.00")
        self.assertEqual(Bed.objects.filter(room=room1).count(), 3)

        # Create A1 room, should create 1 bed
        room2 = Room.objects.create(room_number="A1-01", room_type="A1", price="3000.00")
        self.assertEqual(Bed.objects.filter(room=room2).count(), 1)

    def test_new_room_view_by_superuser(self):
        self.client.force_login(self.superuser)
        url = reverse('hstl:new_room')
        
        # Get request should render form
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'root/newRoom.html')

        # Post request should create room and beds
        data = {
            'room_number': 'A2-02',
            'room_type': 'A2',
            'price': '2500.00'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('hstl:root_index'))

        room = Room.objects.get(room_number='A2-02')
        self.assertEqual(room.room_type, 'A2')
        self.assertEqual(Bed.objects.filter(room=room).count(), 2)

    def test_info_room_view_by_superuser(self):
        self.client.force_login(self.superuser)
        room = Room.objects.create(room_number="A3-03", room_type="A3", price="2800.00")
        
        url = reverse('hstl:info_room', args=[room.id])
        
        # Get request should render form with instance data
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'root/infoRoom.html')

        # Post request should update room details
        data = {
            'room_number': 'A3-03',
            'room_type': 'A3',
            'price': '3000.00'  # updated price
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('hstl:root_index'))

        room.refresh_from_db()
        self.assertEqual(room.price, 3000.00)

    def test_room_views_redirect_non_superuser(self):
        # Test anonymous user
        new_room_url = reverse('hstl:new_room')
        response = self.client.get(new_room_url)
        self.assertRedirects(response, reverse('hstl:index'))

        # Test regular student user
        self.client.force_login(self.student)
        response = self.client.get(new_room_url)
        self.assertRedirects(response, reverse('hstl:index'))

