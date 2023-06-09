import pytest
from django.core.exceptions import ValidationError
from apps.core.users.models import CustomUser

@pytest.mark.parametrize(
    "username, email, password, user_type", 
    [
        ("testuser1", "test1@example.com", "password1", "CLI"),
        ("testuser2", "test2@example.com", "password2", "STF"),
        ("testuser3", "test3@example.com", "password3", "ADM"),
        ("testuser4", "test4@example.com", "password4", "SADM"),
        ("testuser5", "test5@example.com", "password5", "PRV"),
    ]
)
def test_custom_user_model(username, email, password, user_type):
    """
    Test the creation of a CustomUser model instance and its fields' validation.

    :param username: Username of the user
    :param email: Email of the user
    :param password: Password of the user
    :param user_type: Type of user (Cliente, Staff, Admin, Superadmin, Proveedor)
    """
    user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type)
    
    assert user.username == username
    assert user.email == email
    assert user.check_password(password)
    assert user.user_type == user_type

    # Test field validation
    with pytest.raises(ValidationError):
        user.username = ""
        user.full_clean()
    with pytest.raises(ValidationError):
        user.email = ""
        user.full_clean()
