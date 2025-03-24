# 13. Tambahkan Unit Testing untuk Service Layer di tests.py
import pytest
from .services import UserService, ProductService
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_register_user():
    user = UserService.create_user(username='testuser', email='test@example.com', password='password')
    assert user.username == 'testuser'

@pytest.mark.django_db
def test_create_product():
    product = ProductService.create_product(name='Test Product', description='A test product', price=99.99)
    assert product.name == 'Test Product'
