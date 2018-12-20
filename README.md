# Refugee Demographic & Connectivity Trends in Greece and Serbia

## Purpose:
The main objective of this database is to improve the understanding of European refugees’ and displaced communities’ access to the internet and mobile device ownership from a high-level perspective. Access to information is becoming a higher priority for humanitarian agencies that aid refugees “vital to the sense of security and wellbeing through the process”<sup>1</sup> of immigration and it is important to make available a summative quantitative dataset that can be expanded upon and used by those who are addressing the information needs of these marginalized communities. I hope that with this project, this database will be ready for publication on web, so that this topic can be further explored other academics and professionals. 

## Data set:
I have formulated a MySQL database by compiling monthly Cisco Meraki router data and UNHCR (UN High Commissioner for Refugees) refugee camp site profiles that will allow comparison of demographic data and Wifi usage trends in each of the refugee camps profiled. This database consists of information from 20 Greek camps and 9 Serbian ones from a sporadic spread of months ranging from April 2016 to September 2018. This project will coincide with my thesis project for MTOP. 

## Data model
Below ERD diagram a representation of the database that I created. There are 11 tables for this model, as well as many-to-many relationships between monthly_usage_per_camp and nationality, and between monthly_usage_per_camp and application_category (in the diagram, these are respectively joined by refugee_nationality and application_usage tables).

![Logical model of Refugee database](/static/img/model.png "Logical model if refconn")

## Package Dependencies
* Python 3 
* MySQL
* See requirements.txt for necessary Python modules

<br>
<sup>1</sup>Harney, N. (2013). Precarity, affect and problem solving with mobile phones by asylum seekers, refugees and migrants in Naples, Italy. Journal of Refugee Studies, 26(4), 541-557.
