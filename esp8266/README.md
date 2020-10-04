# ESP8266
For a tutorial on getting started with the WeMos D1 mini ESP8266 board, see https://www.instructables.com/Wemos-ESP8266-Getting-Started-Guide-Wemos-101/. In addition to this, you will also need to install the [NeoGPS library](https://github.com/SlashDevin/NeoGPS). When you program the ESP8266 remember to set the SPIFFS to 3 MB for maximum log capacity.

## Configuration

The following has to be configured in the code:

* Wifi credentials
* Domain name of website where data is sent
* MD5 salt - remember that this should be identical to the one set on the website