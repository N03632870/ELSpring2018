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

**Third Step: Set up Pi to read data**
1. 
