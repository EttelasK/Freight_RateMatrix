from django import forms
from .models import *

class NewCarrier(forms.ModelForm):
    class Meta:
        model = Carrier
        fields = ('name',)

class NewLocation(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('city', 'state', 'zip')

class NewLane(forms.ModelForm):
    origin = forms.ModelChoiceField(queryset=Location.objects.all())
    destination = forms.ModelChoiceField(queryset=Location.objects.all())
    miles = forms.IntegerField()
    class Meta:
        model = Lane
        fields = ('origin', 'destination', 'miles')
def __init__(self):
    super(NewLane, self).__init__()

class ViewRate(forms.Form):
    origin = forms.ModelChoiceField(queryset=Location.objects.all())
    destination = forms.ModelChoiceField(queryset=Location.objects.all())
def __init__(self):
    super(ViewRate, self).__init__()

class NewRate(forms.ModelForm):
    origin = forms.ModelChoiceField(queryset=Location.objects.all())
    destination = forms.ModelChoiceField(queryset=Location.objects.all())
    carrier = forms.ModelChoiceField(queryset=Carrier.objects.all())
    rate = forms.DecimalField()
    class Meta:
        model = LaneRate
        fields = ('carrier', 'origin', 'destination',  'rate')
def __init__(self):
    super(NewRate, self).__init__()

class ContactInfo(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('full_name', 'email', 'phone', 'company')