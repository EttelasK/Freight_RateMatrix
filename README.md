Freight Matrix Portal, Web Application
======================
+ Created: March 2016

# Overview
The Freight Matrix Portal web application (rate matrix app) is a front end user interface application to manage freight carriers’ rates and lanes.  The application allows for monitoring current rates as well as documenting changes in rates for carriers.  The application is written in python and uses the django framework.  Documentation on the django framework can be viewed [here.](https://www.djangoproject.com/)

# Form Data
Location: 
-----------
Location is used as a way to provide origin and destination for each carrier’s lane.  The table returns a ‘City State’ string.  The Location table has the following fields:
-	City:  Character Field, max length = 100, required
-	State = US States Field, required
-	Zip = US Zip Code Field, not required

Carrier: 
-----------
Carrier is used to store what carriers will be used and what lanes/ rates are associated with that carrier. This table returns a ‘Name’ string.  The Carrier table has the following fields:
-	Name: character field, max length = 50, required
-	Add_date: date/time field, auto generated current date

Contact: 
-----------
Contact is used as a way to store specific personal information on each of the carriers.  This information is used to send email to carriers when rates are approved and/ or changed.  The table returns a ‘Contact_Name Company’ string (ex: John UPS).  The Contact table has the following fields:
-	Full_name: Character Field, max length = 100, required
-	Email: Email Field, max length = 254, required
-	Phone: Character Field, max length = 14, required
-	Company: ForeignKEY set to Carrier ID
-	Add_date: date/time field, auto generated current date
-	Update_date: date/time field, auto generated current date

Lane: 
-----------
Lane takes two locations and saves one as an origin and one as a destination.  The table returns a ‘Origin to Destination’ string. Lane table has the following fields:
-	Origin: Character Field, Query Set of ForeignKEY set to Location ID, required
-	Destination: Character Field, Query Set of ForeignKEY set to Location ID, required
-	Miles: Integer field, default value = 0, required
-	Add_date: date/time field, auto generated current date

Rate: 
-----------
Rate takes a carrier from the carrier table, a lane from the lane table, lane type, and can create/ update/ remove a rate for a specific carrier, lane and lane type.  Lane types are a single selection of either Partial lane, Round trip lane or One Way lane.  Returns a string ‘Lane Carrier Rate’ (ex: Chicago, IL to Washington, DC UPS 1.99).  Rate table has the following fields:
-	Lane: ForeignKEY set to Lane ID
-	Carrier: ForeignKEY set to Carrier ID
-	Rate: Decimal Field, max length = 4, default = 0.0, decimal places = 2
-	Type = Character Field, radio list [‘One Way’, ‘Round Trip’, ‘Partial’]
-	User = Character Field, generated from user login request.
-	Old_rate: Decimal Field, max length = 4, default = 0.0, decimal places = 2
-	Add_date: date/time field, auto generated current date
-	Flat_Charge: Rate * (Table = Lane, Column = Miles)

# Database Schematic Architecture
![alt text](https://github.com/EttelasK/Freight_RateMatrix/blob/master/readme_img/architecture.png)

# Page Navigation Flow Chart
![alt text](https://github.com/EttelasK/Freight_RateMatrix/blob/master/readme_img/page_flow.png)

Page, Index (Rate Viewer):
----------
Rate viewer allows user to view rates through a form.  User enters origin, destination and type of lane and selects “View Rates” button.  The site retrieves the distance of the lane, the average fuel price and a rates table for each carrier with a rate in that lane.  The fuel surcharge is a dynamic number based on the weekly fuel average form the US Department of Energy site.   The Carrier names in the table header are links to the Carrier page with a request for the carrier’s id.  
Index: forms
There are three forms at the bottom of the screen which the user may open one at a time or all three.  The first form allows the user to add a carrier.  The form returns an error notification and highlights the required field if submitted incorrectly. 
  				 
The second form allows the users to add a new lane based on origin, destination and miles between. The form returns an error notification and highlights the required field if submitted incorrectly.  The user also has the option of adding a new location if the location is not in the query set list.  The form also only allows a decimal number to be entered into the decimal field. 
  			 

The third form allows the user to add a new rate (or update an existing one).  The user will select an origin and destination (which defaults to the last search from the Rate Viewer form) from a list of all locations, select a carrier from the list of all carriers, select the lane type and enter the rate.  All fields are required from this form.  If an invalid lane is entered into the form, the page displays an error alert at the top of the page notifying the user of an incorrect entry.
  			 

Page, Locations:
----------
Locations page allows the user to view all the locations through a table of city, state and zip code.  
There is one form at the bottom of the screen which the user may open.  This form allows the user to add a new location.  The form returns an error notification and highlights the required field if submitted incorrectly. 


Page, Fuel Surcharge:
----------
The fuel surcharge page allows the user to view this week’s National U.S. Average price per gallon and see what the associated fuel surcharge is.  The National U.S. Average is scrapped from the [U.S. Energy Information Administration.](http://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm) There is a link to the website on the fuel surcharge page where the “This week’s National U.S. Average is: $X.XXX.” is displayed.  This calculated fuel surcharge price is used and displayed on the Home (index) page when using the Rate View form to calculate the total estimated cost. 
 
Page, Rate History:
----------
The rate history page displays all the records of when a rate was entered.  
 
Page Carrier:
----------
The carrier page is a personal profile for each carrier company.  The page lists any contact information for that company and allows the user to change/ update the company’s name or contact information.  The contact information is used to email new/ updated rates to the carriers.  
 
In order to email rates out to carrier contacts, the following will need to be updated in the settings.py file:
  ```python
    EMAIL_HOSTS = ''
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = 
    EMAIL_USE_TLS = True 
  ```

Carrier: Forms
----------
The contacts form on the page allows the user to add any new contact for that company.  The form generates an error message for invalid entries.
 





