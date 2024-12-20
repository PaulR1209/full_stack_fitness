from django.db import models


# Create your models here.


class Membership(models.Model):
    """Represents a membership type in the database"""

    MEMBERSHIP_TYPES = (("Bronze", "Bronze"), ("Silver", "Silver"), ("Gold", "Gold"))

    membership_type = models.CharField(max_length=100, choices=MEMBERSHIP_TYPES)
    price = models.IntegerField()
    description = models.TextField()
    stripe_price_id = models.CharField(max_length=50)

    def __str__(self):
        return self.membership_type
