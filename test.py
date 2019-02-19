import gmapslocsharing
import json

# google account locations are shared with
username = ''
password = ''

# test location for storing cookie. replaced by HA via google_maps.
cookie_output = ''

gm = gmapslocsharing.GoogleMaps(username, password, cookie_output)

gm.run()

# you can test output by using the below:

for person in gm.location.data:
    print(json.dumps(person, sort_keys=False, indent=2))

gm.location.people[0].full_name
