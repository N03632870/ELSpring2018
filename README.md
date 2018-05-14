![New Paltz Logo](misc/newpaltzlogo.jpg)
# Spring 2018 Embedded Linux class.

This repository documents my class work and projects done for _**CPS342**_.

1. **Personal Information**

      Name: *Damian Depuy* 

      Major: *Computer Science* 

      ID: [N03632870](https://github.com/N03632870) 

      Year: *Senior*  

2. **Class Start Date:** Jan 22, 2018

3. **Class End Date:** May 8, 2018

**Sensor Box** Project

This project's goal was to create a web server that hosts a website that can display temperature and humidity data. This data is collected from a raspberry Pi using a DHT22 sensor. The webserver uses Flask as a framework and the data is stored locally on the server using python and Sqlite3 database. There are currently two raspberry Pi's that read data. The BlackBox pi currently reads data and stores it locally on the device. The ClearBox pi reads the data and makes a MQTT connection to the BlackBox and tells it to make an entry into the same database file under a different table. Each pi records data at different intervals. ClearBox runs at minutes 5,20,35,50 of each hour while BlackBox runs at 0,15,30, and 45. 

The web interface asks for a username, password, max count, zone (what pi data to check), and a date-time range. Once submitted, a graph is displayed using Chart.js with a table that continues that data requested. 

This project was completed by one member, Damian Depuuy
