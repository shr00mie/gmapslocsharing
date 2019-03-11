from gmapslocsharing import GoogleMaps
import os
import json

user = os.environ['USER']
path = '/home/{}/.gmtest'.format(user)
cookie = '.google_cookie'

# google account locations are shared with
login = ''
password = ''

# test location for storing cookie. replaced by HA via google_maps.
# cookie_output = '/home/{}/.google_cookie'.format(user)

gm = GoogleMaps(    login=login,
                    password=password,
                    config_path=path,
                    cookie_name=cookie,
                    country='US',
                    debug=False)

gm.location.update()

for person in gm.location.people:
    print(person)
