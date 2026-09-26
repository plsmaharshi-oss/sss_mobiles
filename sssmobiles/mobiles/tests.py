from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from openpyxl import Workbook

from .models import Mobile


class MobileViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='manager', password='safe-password')
        self.client.force_login(self.user)

    def test_add_mobile_rejects_invalid_price(self):
        response = self.client.post(reverse('add_mobile'), {
            'brand': 'Google', 'model_name': 'Pixel 8', 'ram': '8GB',
            'storage': '128GB', 'price': 'not-a-price', 'condition': 'Good',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Mobile.objects.count(), 0)
        self.assertContains(response, 'Enter a number.')

    def test_add_mobile_creates_valid_record(self):
        response = self.client.post(reverse('add_mobile'), {
            'brand': 'Google', 'model_name': 'Pixel 8', 'ram': '8GB',
            'storage': '128GB', 'price': '45000.00', 'condition': 'Good',
            'description': 'Excellent camera',
        })

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Mobile.objects.count(), 1)

    def test_inventory_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('home'))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('home')}")

    def test_excel_import_requires_review_then_creates_records(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(['brand', 'model_name', 'ram', 'storage', 'price', 'condition', 'description'])
        sheet.append(['Apple', 'iPhone 15', '6GB', '128GB', 60000, 'Like New', 'Imported item'])
        content = BytesIO()
        workbook.save(content)
        upload = SimpleUploadedFile(
            'inventory.xlsx', content.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

        review = self.client.post(reverse('import_mobiles'), {'excel_file': upload})
        self.assertEqual(review.status_code, 200)
        self.assertContains(review, 'iPhone 15')
        self.assertEqual(Mobile.objects.count(), 0)

        response = self.client.post(reverse('confirm_import'))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Mobile.objects.count(), 1)

    def test_all_inventory_pages_render(self):
        mobile = Mobile.objects.create(
            brand='Samsung', model_name='Galaxy S24', ram='8GB', storage='256GB',
            price='52000.00', condition='New',
        )

        for url_name, args in (
            ('home', ()), ('add_mobile', ()), ('import_mobiles', ()),
            ('edit_mobile', (mobile.id,)), ('delete_mobile', (mobile.id,)),
        ):
            response = self.client.get(reverse(url_name, args=args))
            self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)
