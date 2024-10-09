from django.db import models
from django.contrib.auth.models import User
from membership.models import Membership

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
