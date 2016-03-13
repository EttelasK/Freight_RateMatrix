import urllib
from BeautifulSoup import *

url = "http://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm"
html = urllib.urlopen(url).read()

soup = BeautifulSoup(html)
tags = soup('td')

fuel_rates = list()

for tag in tags:
    if tag.get('class') == "Current2":
        fuel_rates.append(tag.contents)
fuel = float(str(fuel_rates[len(fuel_rates)-2])[3:8])

print fuel




