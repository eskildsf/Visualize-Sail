from flask import Flask, request, abort, render_template, Response
from hashlib import md5
import os, sys, json, csv

DATA_DIRECTORY = 'data/' # Update this line
TILE_DOMAIN = 'http://tile.yourdomain.tld' # Update this line

## Sentry is optional - Set it up and receive notifications if an exception on the website occours
SENTRY_API_KEY = None # Update this line

# Spontit is optional - Create an account and fill in the information below to receive push notifications on your smartphone
SPONTIT_API_KEY = None # Update this line
SPONTIT_USER_ID = None # Update this line

# MD5 salt is required - Protects you from unauthorized uploads of data
MD5_SALT = b'2J5Pq1lFga' # Update this line, you can use https://www.random.org/strings/?num=1&len=10&digits=on&upperalpha=on&loweralpha=on&unique=on&format=html&rnd=new

if SENTRY_API_KEY is not None:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration
    sentry_sdk.init(dsn = SENTRY_API_KEY, integrations = [FlaskIntegration()])

if SPONTIT_API_KEY is not None and SPONTIT_USER_ID is not None:
    import requests
    spontit_headers = {'X-Authorization': SPONTIT_API_KEY, 'X-UserId': SPONTIT_USER_ID}

# ---

def hms_to_s(h, m, s):
    '''Convert hours, minutes and seconds into seconds.'''
    h, m, s = int(h), int(m), int(s)
    return h*60**2 + m*60 + s

def interpret(path):
    '''Read CSV file and convert to JSON for ease of use in the frontend.'''
    output = []
    with open(path) as f:
        doc = csv.reader(f, delimiter=',')
        next(doc)
        for lat, lng, t, speed, heading in doc:
            ts = hms_to_s(*t.split(':'))
            output.append({'lat':lat, 'lng':lng, 'meta':{'time':ts}})
    return json.dumps(output)

# ---

app = Flask(__name__)

@app.route('/esp8266/<md5hash_esp8266>/<filename>', methods=['POST'])
def upload(md5hash_esp8266,filename):
    '''Receive data from ESP8266 and verify integrity by comparing MD5 hash reported by the ESP8266 with that of the received data. If OK, save to disk.'''
    md5hash_local = md5(MD5_SALT+request.data).hexdigest()    
    if md5hash_esp8266 == md5hash_local:
        path = DATA_DIRECTORY+filename
        with open(path, 'ab') as f: # Append to file
            f.write(request.data)
        if SPONTIT_API_KEY is not None and SPONTIT_USER_ID is not None:
            if md5hash_esp8266 != md5(MD5_salt+'').hexdigest(): # Not empty
                requests.post('https://api.spontit.com/v3/push', json={'message': filename, 'pushTitle': 'Boat',}, headers=spontit_headers)
        return (md5hash_local, 200)
    return abort(404)

@app.route('/json/<filename>', methods=['GET'])
def coordinates(filename):
    '''Serve GPS logs as JSON for rendering at the website.'''
    path = DATA_DIRECTORY+filename
    if os.path.isfile(path):
        return Response(interpret(path), mimetype='application/json')
    return abort(404)

@app.route('/', methods=['GET'])
def index():
    '''Serve the website.'''
    files = [filename for filename in os.listdir(DATA_DIRECTORY) if '.txt' in filename]
    return render_template('index.html', files=files, tile_domain=TILE_DOMAIN)

if __name__ == '__main__':
    TILE_DOMAIN = 'https://a.tile.openstreetmap.org'
    app.run(host='0.0.0.0', port=8080, debug=True)