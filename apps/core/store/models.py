from django.db import models
from django.db.models.manager import Manager
from model_utils.models import (
    TimeStampedModel,
    SoftDeletableModel
)
import re
from django.core.exceptions import ValidationError
from apps.core.store.store_code_gen import StoreCodeGen

class StoreBaseModel(SoftDeletableModel, TimeStampedModel):    
    """
    Abstract base class that extends Django's SoftDeletableModel and TimeStampedModel
    """
    class Meta:
        abstract = True


class StoreModel(StoreBaseModel):
    """
    Model class that extends the StoreBaseModel, representing a store.

    The class has a store code, which is unique and must follow the format: <prefix><5 or 9 digits><4 letter>
    """

    STORE_CODE_PREFIX = ''

    store_code = models.CharField(
        max_length=50,
        verbose_name=_('Store Code'),
        unique=True,
        blank=False,
        null=False
    )

    all_objects = Manager()

    @classmethod
    def gen_strcode(cls):
        """
        Class method that generates a new store code using the StoreCodeGen class
        """
        storecode = StoreCodeGen()
        return storecode.gen_storecode(cls.STORE_CODE_PREFIX)
    
    @classmethod
    def copy_instance(self, cls):
        """
        Class method that creates a copy of a store instance with a new store code.
        """
        cls.id = None
        cls.store_code = cls.gen_storecode()
        return cls.save()
    
    def clean(self):
        """
        Method that validates the store code. The code must follow the format <prefix><5 or 9 digits><1 letter>.
        """
        # Skip O in order to avoid confusing letters
        if self.store_code:
            if not self.store_code or \
                not re.match('^%s\d{9}([A-N]|[P-Z])[a-zA-Z]{4}$' % self.STORE_CODE_PREFIX, str(self.store_code)) and \
                    not re.match('^%s\d{5}([A-N]|[P-Z])[a-zA-Z]{4}$' % self.STORE_CODE_PREFIX, str(self.store_code)):
                        raise ValidationError(
                            {'store_code': ('Enter a value with this format %s<5 or 9 digits><4 letter>'
                                            % self.STORE_CODE_PREFIX)}, code='invalid'
                        )

    class Meta:
        abstract = True