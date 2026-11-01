import uuid
from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from companys.models import Company
from customers.models import CustomerUserProfile
from managers.models import ManagerUserProfile
from assets.models import Customer_RO_Purifier

User = get_user_model()

class PurifierTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create Company A
        self.company_a = Company.objects.create(
            company_name="Company A", slug="company-a", email="a@test.com"
        )
        # Create Company B
        self.company_b = Company.objects.create(
            company_name="Company B", slug="company-b", email="b@test.com"
        )
        
        # Create Manager for Company A
        self.manager_user = User.objects.create_user(email="manager_a@test.com", password="password123")
        ManagerUserProfile.objects.create(user=self.manager_user, company=self.company_a, name="Manager A")
        
        # Create Regular User for Company A
        self.user_a = User.objects.create_user(email="user_a@test.com", password="password123")
        
        # Create User for Customer A
        self.cust_user_a = User.objects.create_user(email="cust_a@test.com", password="password123")
        self.customer_a = CustomerUserProfile.objects.create(
            user=self.cust_user_a, company=self.company_a, name="Customer A", customer_code="A-CUST-1"
        )
        
        # Create User for Customer B
        self.cust_user_b = User.objects.create_user(email="cust_b@test.com", password="password123")
        self.customer_b = CustomerUserProfile.objects.create(
            user=self.cust_user_b, company=self.company_b, name="Customer B", customer_code="B-CUST-1"
        )

        # Create an existing purifier for Company A
        self.purifier_a = Customer_RO_Purifier.objects.create(
            company=self.company_a,
            item_code="ITEM-A1",
            serial_number="SN-A1",
            model_name="Model A",
            customer=self.customer_a,
            purchase_date=date(2023, 1, 1),
            installation_date=date(2023, 1, 5),
            warranty=12,
            warranty_ending_date=date(2024, 1, 5),
            last_service_date=date(2023, 6, 1)
        )
        
        # Create an existing purifier for Company B
        self.purifier_b = Customer_RO_Purifier.objects.create(
            company=self.company_b,
            item_code="ITEM-B1",
            serial_number="SN-B1",
            model_name="Model B",
            customer=self.customer_b,
            purchase_date=date(2023, 1, 1),
            installation_date=date(2023, 1, 5),
            warranty=12,
            warranty_ending_date=date(2024, 1, 5),
            last_service_date=date(2023, 6, 1)
        )

    def test_list_purifiers_isolation(self):
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get(f'/api/company-a/purifiers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['serial_number'], "SN-A1")

    def test_list_purifiers_filter_customer(self):
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get(f'/api/company-a/purifiers/?customer_id={self.customer_a.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        response = self.client.get(f'/api/company-a/purifiers/?customer_id={self.customer_b.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_purifier_authorized(self):
        self.client.force_authenticate(user=self.manager_user)
        data = {
            "item_code": "ITEM-A2",
            "serial_number": "SN-A2",
            "model_name": "Model A2",
            "customer": self.customer_a.id,
            "purchase_date": "2023-01-01",
            "installation_date": "2023-01-05",
            "warranty": 12,
            "warranty_ending_date": "2024-01-05",
            "last_service_date": "2023-06-01"
        }
        response = self.client.post(f'/api/company-a/purifiers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer_RO_Purifier.objects.filter(serial_number="SN-A2").count(), 1)

    def test_create_purifier_unauthorized(self):
        self.client.force_authenticate(user=self.user_a)
        data = {
            "item_code": "ITEM-A2",
            "serial_number": "SN-A2",
            "model_name": "Model A2",
            "customer": self.customer_a.id,
            "purchase_date": "2023-01-01",
            "installation_date": "2023-01-05",
            "warranty": 12,
            "warranty_ending_date": "2023-06-01",
            "last_service_date": "2023-06-01"
        }
        response = self.client.post(f'/api/company-a/purifiers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_purifier_cross_tenant_customer(self):
        self.client.force_authenticate(user=self.manager_user)
        data = {
            "item_code": "ITEM-A2",
            "serial_number": "SN-A2",
            "model_name": "Model A2",
            "customer": self.customer_b.id,  # Customer from Company B
            "purchase_date": "2023-01-01",
            "installation_date": "2023-01-05",
            "warranty": 12,
            "warranty_ending_date": "2024-01-05",
            "last_service_date": "2023-06-01"
        }
        response = self.client.post(f'/api/company-a/purifiers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('customer', response.data)

    def test_detail_purifier_isolation(self):
        self.client.force_authenticate(user=self.user_a)
        # Valid access
        response = self.client.get(f'/api/company-a/purifiers/{self.purifier_a.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Accessing Company B's purifier via Company A's slug
        response = self.client.get(f'/api/company-a/purifiers/{self.purifier_b.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_purifier_authorized(self):
        self.client.force_authenticate(user=self.manager_user)
        data = {"model_name": "Updated Model A"}
        response = self.client.put(f'/api/company-a/purifiers/{self.purifier_a.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purifier_a.refresh_from_db()
        self.assertEqual(self.purifier_a.model_name, "Updated Model A")

    def test_update_purifier_unauthorized(self):
        self.client.force_authenticate(user=self.user_a)
        data = {"model_name": "Hacker Update"}
        response = self.client.put(f'/api/company-a/purifiers/{self.purifier_a.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
