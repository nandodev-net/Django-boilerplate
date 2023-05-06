from django.db import models
from apps.core.store.models import StoreModel
from django.core.exceptions import ValidationError


class Company(StoreModel):
    STORE_CODE_PREFIX = "COMP"

    doctypes = (
        ('TIN', 'TIN'),
        ('IRS', 'IRS'),
        ('EIN', 'EIN'),
        ('SSN', 'SSN'),
    )

    name = models.CharField(
        max_length=50,
        verbose_name=('Company Name'),
        unique=False,
        blank=False,
        null=False
    )

    tax_document = models.CharField(
        max_length=50,
        verbose_name=('Last 4 digits TIN/IRS/EIN/SSN'),
        unique=True,
        blank=True,
        null=True
    )

    doctype = models.CharField(
        max_length=30,
        choices=doctypes,
        default='SSN',
    )

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def save(self, *args, **kwargs):
        MAX_TRIES = 10
        tries = 0
        while tries < MAX_TRIES:
            try:
                self.store_code = self.gen_strcode()
                super(Company, self).save(*args, **kwargs)
            except Exception as e:
                # If an error occurs, print an error message and retry
                tries += 1
                print("Error adding Company instance. Trying again ({}/{}): {}".format(tries, MAX_TRIES, e))
         # If the maximum number of retries is reached and the request still fails, return Exception
        raise ValidationError("Failed to save Company instance after {} tries".format(MAX_TRIES))