This directory will hold all the documentation I create for my project.

Initial Progress Report of the Project- Progress.txt

This documentation is a quick guide on how the project was created.

**Parts used:**

* 1 hdmi cable and mouse/keyboard set for initial installation of OS
* 2 Debug cables for Raspberry Pi USB to TTL Serial Cables
* 2 Raspberry Pi 3 eModel B Motherboards each with
* 2 DHT22/AM2302 Digital Temperature and Humidity Sensors
* 2 Raspberry Pi case (one black, one clear)
* 2 400 Points breadboard about 3.2" x 2.1" x 0.3"
* 8 Jumper wire ribbon cables, male-female ends
* 4 1/4-watt 200ohm resistors
* 2 LEDs
   
This documentation assumes reader has some prior knowledge of linux and raspberry pi installation. It is not meant to be a complete tutorial. I will use narration to explain the what I have done up until presentation day.

**First Step: Set up two Raspberry Pi's**

1. Using the link: [Installing OS Images](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) I used Etcher to burn Raspbian to the external MicroSD card.When completed, the card gets inserted into a pi where I can now access it from a monitor using HDMI and plugging in a keyboard and mouse to navigate. 

2. After the install, I can now either use the debug usb cables to connect to the console directly, or continue using the HDMI setup.

**Second Step: Set up DHT22 sensors**

1. (With power off for safety)Connect jumpers to pins #1 (3.3v to power sensor), #9 (ground), #11 (GPIO 17 data for the LED), #13 (GPIO 27 for sensor data)
2. I connected the wires into a breadboard making sure i attach a resister between the power and data pins of the DHT22 sensor.
3. The LED's negative end can have a resistor connect between the negative jumper and the negative pin of the DHT22 sensor. The positive end goes to the wire connected to the #11 GPIO 17 pin.

**Third Step: Set up Pi to read data, act as server and listen for other Pi**
1. (both Pis) I used Adafruit_DHT library to read the data sensors. [adafruit.com](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/software-install-updated)
2. I used sqlite3 as my database. $ sudo apt-get install sqlite3 This can be installed on all pis but I chose BlackPi to store the date and run the webserver. 

3. Flask framework was used to create the webserver. Various ways to install [Flask](http://flask.pocoo.org/docs/0.12/installation/)
4. Both Pi's need a package called paho–mqtt. This allows each pi to communicate through messaging. this can be installed with $ sudo apt-get install mosquitto mosquitto-clients python-mosquitto

**Fourth Step: write code and test project**
1. Located in the /code directory is a file called dataDHT22.py which is given to the ClearPi that does not contain the webserver. The data is read and sent over as a MQTT message that the BlackPi reads, and inputs the data into its local database. This same code is also used in the Black Pi, but with the comments left out and the database table changed to data01 instead of data02. Both Pis run a crontab schedule of running the code every 15 minutes. BlackPi at intervals 0,15,30,45 and ClearPi at intervals 5,20,35,50.
2. In the /code/Database folder the client.py script is responsible for receiving the messages and inserting the data to the dth22.db file that contains all the database data.
3. In the Project_Spring2018 folder, the WebServer.py is executed so that the web interface can display the data. Depending on the selections from the Login page, the display will show in both table form and line graph form.

**Fifth step: Run the code, wait, and query**
1. Each Pi needs to be on the same wireless network to communicate and the ip address is needed for each pi. 
2. The webserver is also on the closed network with on port 900. 

** Known bugs **
1. Chart.js used for the web inteface doesn't show legend, or labels when it is supposed to.
2. If the power supply is weak, wifi may not work. Try and use fast-charger style supplies.
3. Something in the code doesn't allow for the blinking light when MQTT recieves data (BlackPi). LED works otherwise suggesting a code issue in the client.py script. 
4. Flask bootstrap doesn't quite work on mobile devices. This is usually a javaScript issue and is common and easy to fix.

** What the project needed to do **
1. The project had issues connecting to the Newpaltz schools wireless network. I used a wifi workaround involving my personal phone's wifi network.
2. Data needs to be shown in real time on the webpage.
3. date-picker in the login feature is not as clean as I wanted. Issues resulted due to the way the data format on the database not matching the exact format of the pickers.
