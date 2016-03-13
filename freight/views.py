from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.exceptions import ValidationError
from django.template import loader, context
from django.core.mail import send_mail
from freight.models import *
from .forms import *
from django.contrib import messages
from django.conf import settings
from bs4 import BeautifulSoup
import urllib

def index(request):
    carrier = Carrier.objects.order_by('name')
    url = "http://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm"
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all('td', {'class': 'Current2'})
    fuel_rates = list()
    for tag in tags:
        fuel_rates.append(tag.text)
    fuel = float(fuel_rates[len(fuel_rates)-2])
    #table range (increments of 0.050 cents)
    min = 1.950
    max = 1.999
    fsc = 0.15
    while max < 5.000:
        if fuel >= min and fuel <=max:
            surcharge = float(round(fsc,3))
        min=min+.050
        max=max+.050
        fsc=fsc+.01

    #Lookup rates for each carrier based on origin and destination on index page
    if request.method == "POST":
        form_lookup = ViewRate(request.POST)
        form_carrier = NewCarrier(request.POST)
        form_lane = NewLane(request.POST)
        form_rate = NewRate(request.POST)

        if form_rate.is_valid():
            new_rate = form_rate.save(commit=False)
            orig_id = request.POST.get('origin','')
            dest_id = request.POST.get('destination','')
            carrier_id = request.POST.get('carrier','')
            carrier = get_object_or_404(Carrier, pk=carrier_id)
            orig = get_object_or_404(Location, pk=orig_id)
            dest = get_object_or_404(Location, pk=dest_id)
            ln = get_object_or_404(Lane, origin=orig, destination=dest)
            ln_rt = LaneRate.objects.filter(lane=ln, carrier=carrier)
            lane = Lane.objects.all()
            if ln in lane:
                if len(ln_rt) > 0:
                    recent_rate = LaneRate.objects.filter(lane=ln, carrier=carrier).order_by('-add_date')[0]
                    recent_rt = recent_rate.rate
                    new_rate.old_rate = recent_rt
                    new_rate.lane = ln
                    new_rate.add_date = timezone.now()
                    new_rate.user = request.user
                    new_rate.save()
                else:
                    new_rate.lane = ln
                    new_rate.add_date = timezone.now()
                    new_rate.user = request.user
                    new_rate.save()
            else:
                raise ValidationError("That lane does not exist.")
            return redirect('freight:index')

        if form_lane.is_valid():
            lane = form_lane.save(commit=False)
            lane_orig = lane.origin
            lane_dest = lane.destination
            ln = Lane.objects.filter(origin=lane_orig, destination=lane_dest)
            if len(ln) > 0:
                raise ValidationError('That lane already exists.')
            else:
                lane.save()
            return redirect('freight:index')

        if form_carrier.is_valid():
            carrier = form_carrier.save(commit=False)
            name = carrier.name
            cr = Carrier.objects.filter(name=name)
            if len(cr)>0:
                raise ValidationError('That carrier already exists.')
            else:
                carrier.add_date = timezone.now()
                carrier.save()
            return redirect('freight:carrier_detail', carrier_id=carrier.id)

        if form_lookup.is_valid():
            orig_id = request.POST.get('origin','')
            dest_id = request.POST.get('destination','')
            orig = get_object_or_404(Location, pk=orig_id)
            dest = get_object_or_404(Location, pk=dest_id)
            check = Lane.objects.filter(origin=orig, destination=dest)
            if len(check)>0:
                ln = Lane.objects.get(origin=orig, destination=dest)
                lane_rate = []
                carriers = []
                lane_search = LaneRate.objects.filter(lane=ln)
                for lc in lane_search:
                    if lc.carrier not in carriers:
                        carriers.append(lc.carrier)
                for c in carriers:
                    latest_rate = LaneRate.objects.filter(lane=ln, carrier=c).order_by('-add_date')[0]
                    lane_rate.append(latest_rate)
                mileage = ln.miles
                total_fuel = mileage * surcharge
                total_fuel = round(total_fuel,3)
            else:
                raise ValidationError('No such lane.')
            context = {'total_fuel':total_fuel, 'surcharge':surcharge, 'fuel':fuel,'carrier': carrier, 'form_lookup':form_lookup, 'mileage':mileage, 'lane_rate':lane_rate, 'form_carrier':form_carrier, 'form_rate':form_rate, 'form_lane':form_lane}
            return render(request, 'freight/index.html', context,)
    else:
        form_lookup = ViewRate()
        form_carrier = NewCarrier()
        form_lane = NewLane()
        form_rate = NewRate()

    context = {'fuel':fuel,'carrier': carrier, 'form_lookup':form_lookup, 'form_carrier':form_carrier, 'form_lane':form_lane, 'form_rate':form_rate}
    return render(request, 'freight/index.html', context,)

def rate_history(request):
    lane_rates = LaneRate.objects.order_by('-add_date')
    new = lane_rates[0:2]
    context={'lane_rates':lane_rates}
    return render(request, 'freight/rate_history.html', context,)

def carrier_detail(request, carrier_id):
    name = get_object_or_404(Carrier, pk=carrier_id)
    carrier = get_object_or_404(Carrier, pk=carrier_id)
    contact_list = Contact.objects.filter(company=carrier)

    try:
        carrier = Carrier.objects.get(pk=carrier_id)
    except Carrier.DoesNotExist:
        raise Http404("No Carrier Available.")

    if request.method == "POST":
        form_carrier = NewCarrier(request.POST, instance=carrier)
        form_contact = ContactInfo(request.POST)

        if form_carrier.is_valid():
            carrier = form_carrier.save(commit=False)
            carrier.add_date = timezone.now()
            carrier.save()
            return redirect('freight:carrier_detail', carrier_id=carrier_id)

        if form_contact.is_valid():
            contact = form_contact.save(commit=False)
            contact.add_date = timezone.now()
            contact.update_date = timezone.now()
            contact.save()
            return redirect('freight:carrier_detail', carrier_id=carrier_id)
    else:
        form_carrier = NewCarrier(instance=carrier)
        form_contact = ContactInfo()

    # subject = 'Site Contact'
    # from_email = settings.EMAIL_HOST_USER
    # to_email = [from_email, 'ksalette@vt.edu']
    # contact_message = "%s:%s via %s" % (carrier, message, form_email)
    # send_mail(subject, contact_message, from_email, [to_email], fail_silently=False)
    context={'name': name, 'contact_list':contact_list, 'form_carrier':form_carrier, 'form_contact':form_contact, 'carrier':carrier}
    return render(request, 'freight/carrier.html', context,)


def location_detail(request, location_id):
    loc = get_object_or_404(Location, pk=location_id)
    try:
        location = Location.objects.get(pk=location_id)
    except Location.DoesNotExist:
        raise Http404("No Location Available.")
    return render(request, 'freight/location.html', {'loc': loc})

def fuel_surcharge(request):
    url = "http://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm"
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all('td', {'class': 'Current2'})
    fuel_rates = list()
    for tag in tags:
        fuel_rates.append(tag.text)
    fuel = float(fuel_rates[len(fuel_rates)-2])
    #table range (increments of 0.50 cents)
    min = 1.950
    max = 1.999
    fsc = 0.15
    while max < 5.000:
        if fuel >= min and fuel <=max:
            surcharge = float(round(fsc,3))
        min=min+.050
        max=max+.050
        fsc=fsc+.01
    return render(request, 'freight/fuel_surcharge.html', {'fuel':fuel, 'surcharge':surcharge})

def location_all(request):
    loc = Location.objects.order_by('city')
    if request.method == "POST":
        form = NewLocation(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.save()
            return redirect('freight:location_all')
    else:
        form = NewLocation()
    context = {'loc': loc, 'form':form}
    return render(request, 'freight/location.html', context)