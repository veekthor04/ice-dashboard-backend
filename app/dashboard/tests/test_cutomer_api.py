from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Customer
from dashboard.serializers import CustomerSerializer

from core.utils import sample_user, sample_customer


CUSTOMER_LIST_URL = reverse("dashboard:customer-list")


def customer_detail_url(customer_id: str):
    """Return the detail url for a customer"""
    return reverse("dashboard:customer-detail", args=[customer_id])


class PublicCustomerAPITests(TestCase):
    """Test the unauthenticated customer api access"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test login is required to access API"""
        res = self.client.get(CUSTOMER_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateCustomerAPITests(TestCase):
    """Test the authenticated customer api access"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(user=self.user)

    def test_create_customer_successful(self):
        """Test customer url to create new customer"""
        payload = {
            "name": "test customer",
            "email": "test@test.com",
            "address": "123 test address",
        }
        res = self.client.post(CUSTOMER_LIST_URL, payload)

        customer = Customer.objects.get(**payload)
        serializer = CustomerSerializer(customer, many=False)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json(), serializer.data)

    def test_create_customer_invalid_data(self):
        """Test customer url to create new customer with invalid data"""
        payload = {
            "name": "",
            "email": "test",
        }
        res = self.client.post(CUSTOMER_LIST_URL, payload)

        serializer = CustomerSerializer(data=payload)
        serializer.is_valid()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json(), serializer.errors)

    def test_list_customer(self):
        """Test customer url to list created customers"""

        sample_customer()
        sample_customer()

        res = self.client.get(CUSTOMER_LIST_URL)

        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.json())
        self.assertEqual(res.json()["results"], serializer.data)

    def test_retrieve_customer_success(self):
        """Test customer url to retrieve a customer"""

        customer = sample_customer()

        url = customer_detail_url(customer.customer_id)
        res = self.client.get(url)

        customer = Customer.objects.get(customer_id=customer.customer_id)
        serializer = CustomerSerializer(customer, many=False)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), serializer.data)

    def test_retrieve_customer_not_found(self):
        """Test customer url to retrieve a customer that doesnot exist"""

        customer_id = "test_id123"

        url = customer_detail_url(customer_id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_customer_detail(self):
        """Test customer url to update a customer's detail"""

        customer = sample_customer(address="123 test address")

        payload = {"address": "123 new test address"}

        url = customer_detail_url(customer.customer_id)
        res = self.client.patch(url, payload)

        customer.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(customer.address, payload["address"])

    def test_delete_customer(self):
        """Test customer url to delete a customer"""

        customer = sample_customer()

        url = customer_detail_url(customer.customer_id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Customer.DoesNotExist):
            Customer.objects.get(customer_id=customer.customer_id)
