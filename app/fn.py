from app.models import *

def make():
    customers = ['WalMart','Target','Altria','PetCo']
    for c in customers:
        co,cr = Customer.objects.get_or_create(name=c)

    cities = ['Austin','Boston','NY','LA','Chicago','DC']

    for c in cities:
        co,cr = City.objects.get_or_create(name=c)

    carriers = ['UPS','FedEx','ShittyXpress']
    for c in carriers:
        co,cr = Carrier.objects.get_or_create(name=c)


    factories = ['A Products','B Inc','C Global']
    for c in factories:
        for i in City.objects.all():
            co,cr = Factory.objects.get_or_create(name=c, city=i)

    parts = ['screw', 'washer', 'bar','spoke','bearing']
    for c in parts:
        co,cr = Part.objects.get_or_create(name=c)

    items = ['bike','rollerblade','skateboard','car']
    for i,c in enumerate(items):
        co,cr = Item.objects.get_or_create(name=c)
        ip = ItemPs.objects.get_or_create(item = co, part=Part.objects.get(id=2))
        ip = ItemPs.objects.get_or_create(item = co, part=Part.objects.get(id=3))
    #warehouse
    for cu in Customer.objects.all():
        for c in City.objects.all():
            wh,cr = Warehouse.objects.get_or_create(city=c,customer=cu)
    #warehouseinventory
    for cu in Item.objects.all():
        for c in Warehouse.objects.all():
            wh,cr = WarehouseInventory.objects.get_or_create(warehouse=c,item=cu)
    #factorypart
    for cu in Part.objects.all():
        for c in Factory.objects.all():
            wh,cr = FactoryPart.objects.get_or_create(factory=c,part=cu)



#lane
