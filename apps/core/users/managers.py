from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    CustomUserManager extends Django's BaseUserManager, adding some functions
    to create users and superusers.
    """

    def create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        
        Args:
            username (str): The username for the user.
            email (str): The email address for the user.
            password (str): The password for the user.
            **extra_fields: Extra fields to include in the creation of the User.
        
        Returns:
            A User instance.
        """
        if not username:
            raise ValueError(_('The Username must be set')) # Validates that the username is set.

        if not email:
            raise ValueError(_('The Email must be set')) # Validates that the email is set.
        email = self.normalize_email(email)

        user = self.model(email=email, username=username, **extra_fields) # Creates a User instance.
        user.set_password(password) # Sets the user's password.
        user.save() # Saves the User instance.
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Creates and saves a Superuser with the given username, email and password.
        
        Args:
            username (str): The username for the superuser.
            email (str): The email address for the superuser.
            password (str): The password for the superuser.
            **extra_fields: Extra fields to include in the creation of the Superuser.
        
        Returns:
            A User instance (with superuser privileges).
        """
        extra_fields.setdefault('is_staff', True) # Ensures the user is marked as staff.
        extra_fields.setdefault('is_superuser', True) # Ensures the user is marked as a superuser.

        return self.create_user(username, email, password, **extra_fields) # Creates a Superuser instance.
