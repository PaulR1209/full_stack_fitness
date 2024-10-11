from django.db import models


# Create your models here.

class Membership(models.Model):
    MEMBERSHIP_TYPES = (
        ('Bronze', 'Bronze'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold')
    )

    membership_type = models.CharField(max_length=100, choices=MEMBERSHIP_TYPES)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.membership_type