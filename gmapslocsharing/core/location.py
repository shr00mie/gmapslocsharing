from collections import namedtuple
from datetime import datetime
from .config import Config
import logging
import json

log = logging.getLogger(__name__)

class Location:

    def __init__(self):

        log.debug('Initializing Location module.')
        self.config = Config()

        self.parsed_people = {}
        self.dict_people = {}
        self.people = []

        self.debug_location = self.config.path_debug / 'location_debug'

    def parse_raw_people(self, raw_people:list) -> dict:
        '''
        Input: self.raw_output list
        Performs: final cleanup of per person raw_output into dictionary of
                  people using id:person as first level keys with key:value per
                  person. regex and error catching for gps, battery, and scenarios
                  where phone is on battery optimization mode.
        Returns: new_people dict containing {person_id:{key:value}}
        '''

        pp = {}

        keep =  {
                0:'id',
                2:'picture_url',
                4:'full_name',
                7:'gps',
                8:'address',
                10:'country',
                20:'first_name',
                21:'battery'
                }

        for raw_person in raw_people:
            raw_person = raw_person.split('"')[1:23]
            for i, item in enumerate(raw_person):
                if i in keep.keys():
                    if i == 0:
                        id = int(item)
                        name = keep[i]
                        pp[id] = {'id': id}
                    if i == 7:
                        item = item.replace(']','').replace('\\n','').split(',')[3:7]
                        pp[id].update(  {
                                        'latitude': float(item[1]),
                                        'longitude': float(item[0]),
                                        'accuracy': int(item[3]),
                                        'last_seen': int(item[2]) / (10**3)
                                        })
                    elif i == 20:
                        if len(item.split(' ')) == 1:
                            pp[id].update({'first_name': item})
                        else:
                            pp[id].update({'first_name': item.split(' ')[0]})
                    elif i == 21:
                        item = item.split('[')[1].split(']')[0]
                        item = item.split(',') if ',' in item else list(item)
                        if len(item) == 1:
                            pp[id].update(  {
                                            'battery_charging': True
                                            if int(item[0]) == 1
                                            else False,
                                            'battery_level': None
                                            })
                        elif len(item) == 2:
                            pp[id].update(  {
                                            'battery_charging': True
                                            if int(item[0]) == 1
                                            else False,
                                            'battery_level': int(item[1])
                                            })
                    else:
                        pp[id].update({keep[i]: item})
        return pp

    def update_people(self, formatted_people:dict) -> dict:
        '''
        Input: dicts from new_people and old_people.
        Performs: additions/deletions to location sharing users and update
                  old_people dict with new values for each person, if they are
                  not null/none and different from existing data.
        Returns: updated old_people dict.
        '''

        np = formatted_people
        op = self.dict_people if len(self.dict_people.keys()) > 0 else {}

        if len(op.keys()) == 0:
            log.debug('Copying new_people to old_people on first run.')
            op = np
            return op
        else:
            if np.keys() != op.keys():
                add = [id for id in np.keys() if len(np.keys()) > 0 and id not in op.keys()]
                remove = [id for id in op.keys() if len(op.keys()) > 0 and id not in np.keys()]
                if len(add) != 0:
                    log.debug('IDs to add: {}'.format(add))
                if len(remove) != 0:
                    log.debug('IDs to remove: {}'.format(remove))
                for id in add:
                    log.debug('Adding {}:{} to old_people.'.format(id, np[id]))
                    op[id] = np[id]
                for id in remove:
                    log.debug('Deleting {}:{} from old_people.'.format(id, op[id]))
                    del op[id]

            elif np.keys() == op.keys():
                log.debug('Comparing new and existing person data.')
                for id, person in np.items():
                    name = person['first_name']
                    for key, value in person.items():
                        new_value = np[id][key]
                        old_value = op[id][key]
                        if new_value != old_value and new_value is not None:
                            log.debug('Updating {} for {} to {}.'.format(key, name, new_value))
                            op[id][key] = np[id][key]
        if len(op.keys()) > 0:
            return op

    def create_people(self, dict_people:dict) -> list:
        '''
        Inputs: person class entity and old_people dict.
        Performs: conversion of old_people into list of named tuples.
        Returns: people objects to be returned back to HA for consumption.
        '''

        people = []
        for id, person in dict_people.items():
            Person = namedtuple('Person', ' '.join([key for key in person.keys()]))
            people.append(Person(**person))
        return people

    def update(self, raw_output):
        '''
        Performs: location update for gmapslocsharing.
        '''

        log.debug('Updating location sharing data.')

        go_on = True

        if go_on:
            try:
                log.debug('Parsing raw people.')
                self.parsed_people = self.parse_raw_people(raw_output)
                self.debug('parsed_people', self.parsed_people)
            except Exception as e:
                log.info('Error parsing raw people: {}.'.format(e))
                go_on=False

        if go_on:
            try:
                log.debug('Updating people.')
                self.dict_people = self.update_people(self.parsed_people)
                self.debug('dict_people', self.dict_people)
            except Exception as e:
                log.info('Error updating people: {}.'.format(e))
                go_on=False

        if go_on:
            try:
                log.debug('Creating {} people.'.format(len(self.dict_people.keys())))
                self.people = self.create_people(self.dict_people)
                self.debug('people', self.people)
                log.debug('Location update completed successfully.')
                return self.people
            except Exception as e:
                log.info('Error converting people: {}.'.format(e))


    def debug(self, source, data):

        if self.config.debug:

            path = self.config.path_debug_location

            if not path.exists():
                path.mkdir(mode=0o770, parents=True)

            timestamp = datetime.now().strftime('%Y-%m-%d - %H:%M:%S')
            parsed_path = path / 'parsed_people'
            dict_path = path / 'dict_people'
            person_path = path / 'people'

            if source == 'parsed_people':
                with parsed_path.open('a+') as f:
                    f.write('{}\n'.format(timestamp))
                    for id, person in data.items():
                        f.write('{}\n'.format(json.dumps(person, sort_keys=False, indent=4)))
                    f.write('\n')

            if source == 'dict_people':
                with dict_path.open('a+') as f:
                    f.write('{}\n'.format(timestamp))
                    for id, person in data.items():
                        f.write('{}\n'.format(json.dumps(person, sort_keys=False, indent=4)))
                    f.write('\n')

            if source == 'people':
                with person_path.open('a+') as f:
                    f.write('{}\n'.format(timestamp))
                    for person in data:
                        f.write('{}\n'.format(json.dumps(person, sort_keys=False, indent=4)))
                    f.write('\n')
