# Website
For a tutorial on how to set up NGINX, uwsgi and server Flask websites on Ubuntu, see https://medium.com/swlh/deploy-flask-applications-with-uwsgi-and-nginx-on-ubuntu-18-04-2a47f378c3d2.

Python dependencies are:
 * [Flask](https://flask.palletsprojects.com/)

Install it by `pip install flask`

JavaScript dependencies are:
 * [Zepto.js](https://zeptojs.com/)
 * [JQuery](https://jquery.com/)
 * [Leaflet](https://leafletjs.com/)
 * [Leaflet.MultiOptionsPolyline](https://github.com/hgoebl/Leaflet.MultiOptionsPolyline)
 * [Leaflet.GeometryUtil](https://github.com/makinacorpus/Leaflet.GeometryUtil)

These are included.

## Configuration

The following has to be configured:

* `uwsgi.ini` 
  * Website directory
  * Socket directory
* `nginx.conf`
  * Path of uwsgi socket
  * Domain name
  * Directory to hold cached OpenStreetMap tiles
* `src/website.py`
  * Data directory
  * Domain of tile website
  * MD5 salt - remember that this should be identical to the one on the ESP8266

You are welcome to also configure [Sentry](https://sentry.io/) and [Spontit](https://spontit.com/) but it is not required.