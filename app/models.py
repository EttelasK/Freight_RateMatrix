from django.db import models
# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=200)
    #warehouse = models.ForeignKey('Warehouse')
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    class Meta:
        ordering = ('name',)

class Carrier(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    class Meta:
        ordering = ('name',)

class City(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    class Meta:
        ordering = ('name',)

class Lane(models.Model):
    start = models.ForeignKey(City,related_name='start')
    end = models.ForeignKey(City,related_name='end')
    carrier = models.ForeignKey(Carrier)
    rate = models.DecimalField(decimal_places=4,max_digits=10,default=0.0)#max_length=10,max_digits=4)
    distance = models.IntegerField(default=0)

class Factory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    city = models.ForeignKey(City)
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    class Meta:
        ordering = ('name',)

class Part(models.Model):
    name = models.CharField(max_length=200)
    #price?
    factories = models.ManyToManyField('Factory', through='FactoryPart')
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    class Meta:
        ordering = ('name',)

class Item(models.Model):
    name = models.CharField(max_length=200)
    weight = models.IntegerField(default=0)
    #size
    parts = models.ManyToManyField('Part', through='ItemPs')
    #price?
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    class Meta:
        ordering = ('name',)

class ItemPs(models.Model):
    item = models.ForeignKey(Item)
    part = models.ForeignKey(Part)
    amt = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
        return "%s - %s"%(self.item.name, self.part.name)

class Warehouse(models.Model):
    city = models.ForeignKey(City)
    inventory = models.ManyToManyField('Item',through='WarehouseInventory')
    customer = models.ForeignKey('Customer',null=True,blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return "%s - %s"%(self.city.name, self.customer.name)


class WarehouseInventory(models.Model):
    item = models.ForeignKey(Item)
    warehouse = models.ForeignKey(Warehouse)
    amt = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
        return "%s"%(self.item.name)#, self.warehouse)



class FactoryPart(models.Model):
    QUAL =(
    (1, 'great'),
    (2, 'ok'),
    (3, 'shitty'),
)
    part = models.ForeignKey(Part)
    factory = models.ForeignKey(Factory)
    quality = models.IntegerField(choices=QUAL,default=2)
    unit_price = models.DecimalField(decimal_places=4,max_digits=10,default=0.0)#max_digits=3,max_length=10)