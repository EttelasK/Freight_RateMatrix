import datetime

from django.db import models
from django.utils import timezone
from localflavor.us.models import USStateField, USZipCodeField

class Carrier(models.Model):
    name = models.CharField(max_length=50)
    add_date = models.DateTimeField('date published')
    lane_rates = models.ManyToManyField('Lane', null=True, blank=True, through='LaneRate')
    def __str__(self):
        return self.name
    def new_added_carriers(self):
        return self.add_date >= timezone.now() - datetime.timedelta(days=1)

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=14)
    company = models.ForeignKey(Carrier)
    add_date = models.DateTimeField()
    update_date = models.DateTimeField()
    def __str__(self):
        return '%s %s'%(self.full_name, self.company)
    def new_contact(self):
        return self.add_date >= timezone.now() - datetime.timedelta(days=1)

class Lane(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    miles = models.IntegerField(default=0)
    def __str__(self):
        return '%s to %s'%(self.origin, self.destination)

class LaneRate(models.Model):
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    rate = models.DecimalField(decimal_places=2,max_digits=4,default=0.0)
    old_rate = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    add_date = models.DateTimeField()
    user = models.CharField(max_length=100)
    def __str__(self):
        return '%s %s %d'%(self.lane, self.carrier, self.rate)
    def flat_charge(self):
        return self.rate * self.lane.miles
    def new_added_rates(self):
        return self.add_date >= timezone.now() - datetime.timedelta(days=7)

class Location(models.Model):
    city = models.CharField(max_length=100)
    state = USStateField(null=True, blank=True)
    zip = USZipCodeField(null=True, blank=True)
    def __str__(self):
        return '%s %s'%(self.city, self.state)
    def __unicode__(self):
        city_st = self.city+', '+self.state
        return city_st
