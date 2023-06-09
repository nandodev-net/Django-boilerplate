from django.contrib.auth.models import AbstractUser
from apps.core.store.models import StoreModel
from apps.core.users.managers import CustomUserManager
from django.db import models

class CustomUser(AbstractUser, StoreModel):    
    """
    CustomUser extends the AbstractUser and StoreModel provided by Django.
    
    This model is designed to cater to different types of users in the eCommerce application,
    including Customers ('CLI'), Staff ('STF'), Admins ('ADM'), SuperAdmin ('SADM'), and Providers ('PRV').
    
    Attributes inherited from AbstractUser:
        username: Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        first_name: Optional. 150 characters or fewer.
        last_name: Optional. 150 characters or fewer.
        email: Optional. Email field.
        password: Required. A hash of, and metadata about, the password.
        groups: Many-to-many relationship to Group
        user_permissions: Many-to-many relationship to Permission
        is_staff: Boolean. Designates whether this user can access the admin site.
        is_active: Boolean. Designates whether this user account should be considered active.
        is_superuser: Boolean. Designates whether this user has all permissions without explicitly assigning them.
        last_login: A datetime of the users last login.
        date_joined: A datetime designating when the account was created. Is set to the current date/time by default.
    
    Attributes inherited from StoreModel:
        store_code: A CharField that stores the unique store code.
    
    Attributes:
        USER_TYPE_CHOICES: A tuple defining the different types of users.
        user_type: A CharField that stores the type of the user.
    
    Inherits from:
        AbstractUser: A fully-featured User model with admin-compliant permissions.
        StoreModel: An abstract base model representing a store, with a unique store code.
    """
    STORE_CODE_PREFIX = "USR"

    USER_TYPE_CHOICES = (
        ('ADM', 'Admin'),
        ('SADM', 'SuperAdmin'),
        ('CLI', 'Client'),
        ('STF', 'Staff'),
        ('PRV', 'Provider'),
    )

    user_type = models.CharField(max_length=3, choices=USER_TYPE_CHOICES)

    # Specifies the field used as the username.
    USERNAME_FIELD = 'username'
    # Lists other fields that will be prompted for when creating a user interactively.
    REQUIRED_FIELDS = ['email',]

    # Assigns the custom user manager to the CustomUser model.
    objects = CustomUserManager()


    def __str__(self):
        return self.email


class UserProfile(StoreModel):
    """
    UserProfile extends the StoreModel to provide additional information about a CustomUser.
    
    This model is designed to store additional user details that are not covered by the CustomUser model,
    such as address, city, country, postal code, and phone number. It is linked to the CustomUser model via a 
    OneToOne relationship, meaning that each user can only have one profile, and each profile can only be 
    associated with one user.
    
    Attributes inherited from StoreModel:
        store_code: A CharField that stores the unique store code.
    
    Attributes:
        STORE_CODE_PREFIX: A constant string used as prefix when generating the store_code.
        user: OneToOne relationship to CustomUser.
        address: CharField to store the user's address. Can be blank.
        city: CharField to store the user's city. Can be blank.
        country: CharField to store the user's country. Can be blank.
        zip_code: CharField to store the user's postal code. Can be blank.
        phone: CharField to store the user's phone number. Can be blank.
    
    Inherits from:
        StoreModel: An abstract base model representing a store, with a unique store code.
    """
        
    STORE_CODE_PREFIX = "USRP"

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=6, blank=True)
    phone = models.CharField(max_length=15, blank=True)