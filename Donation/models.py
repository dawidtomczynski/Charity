from django.contrib.auth.models import User
from django.db import models as m


INSTITUTION_TYPES = {
    (1, 'Fundacja'),
    (2, 'Organizacja pozarządowa'),
    (3, 'Zbiórka lokalna'),
}


class Category(m.Model):
    name = m.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(m.Model):
    name = m.CharField(max_length=255)
    description = m.TextField(blank=True)
    type = m.IntegerField(choices=INSTITUTION_TYPES, default=1)
    categories = m.ManyToManyField('Category')

    def __str__(self):
        return self.name


class Donation(m.Model):
    quantity = m.IntegerField()
    categories = m.ManyToManyField('Category')
    institution = m.ForeignKey('Institution', on_delete=m.CASCADE)
    address = m.CharField(max_length=64)
    phone_number = m.IntegerField()
    city = m.CharField(max_length=64)
    zip_code = m.CharField(max_length=6)
    pick_up_date = m.DateField()
    pick_up_time = m.TimeField()
    pick_up_comment = m.TextField(blank=True)
    user = m.ForeignKey(User, null=True, default=None, on_delete=m.CASCADE)
