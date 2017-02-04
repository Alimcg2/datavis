import json
import requests

with open('ipNames', 'r') as f, open('ipLatLon', 'a') as w:
    base = "http://freegeoip.net/json/"
    for line in f:
        ip = line.strip()
        resp = requests.get(base + ip)
        if resp.status_code != 200:
            print resp.status_code
            continue
        data = json.loads(resp.text)
        lat = data["latitude"]
        lon = data["longitude"]
        countryC = data["country_code"]
        countryN = data["country_name"]
        region = data["region_name"]
        city = data["city"]
        print 'writing ' + ip
        try:
            w.write('%s,%s,%s,%s,%s,%s\n' % (lat, lon, countryC, countryN, region, city))
        except UnicodeEncodeError:
            print 'uncode error on %s, %s %s %s %s' % (ip, countryC, countryN, region, city)
