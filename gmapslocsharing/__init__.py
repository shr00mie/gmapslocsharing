from .core.location import Location
from .core.browser import Browser
from .core.config import Config
from datetime import datetime
from pathlib import Path as p
from shutil import move
import logging
import re

log = logging.getLogger(__name__)

class GoogleMaps:

    def __init__(self, email, password, config_path, debug):

        log.debug('Initializing GoogleMaps module.')
        self.path = p(config_path)
        self.config = Config(self.path, debug)
        self.startup(email, password)
        self.browser = Browser()
        self.location = Location()
        self.people = None
        self.update()

    def startup(self, email, password):

        log.info('Initiating System check.')

        log.debug('Checking email.')
        if self.check_email(email):
            log.debug('Email OK.')
            self.config.set('account', 'email', email)
        else:
            log.debug('Email validation error. Exiting.')

        log.debug('Checking password.')
        if self.check_password(password):
            log.debug('Password OK.')
            self.config.set('account', 'password', password)
        else:
            log.debug('Password validation failed or password too short. Exiting.')

        log.debug('Checking core folders.')
        if self.check_folders():
            log.debug('Core & debug folders OK.')
        else:
            log.debug('Error creating core/debug folders. Exiting.')

    def check_email(self, email:str) -> bool:

        if re.match('^[a-zA-Z0-9].*[a-zA-Z0-9.-].*[a-zA-Z0-9].*\@[a-zA-Z0-9.-].*[a-zA-Z0-9].*\.[a-zA-Z]{2,}$', email):
            return True
        return False

    def check_password(self, password:str) -> bool:

        # TODO: Figure out a better way to check passwords.
        # Maybe kick something back if it's a stupid short password.
        if all([isinstance(password, str), len(password) > 8]):
            return True
        return False

    def check_folders(self) -> bool:

        locations = [
                    self.config.path_chrome,
                    self.config.path_debug,
                    ]
        try:
            for location in locations:
                if all([location.exists(), location.is_dir()]):
                    log.debug('{} exists.'.format(location.as_posix()))
                else:
                    log.debug('Creating {}'.format(location.as_posix()))
                    location.mkdir(mode=0o770, parents=True)
            self.debug_backup()
            return True
        except:
            return False

    def debug_backup(self):

        backup_dt = datetime.now().strftime('%Y.%m.%d_%H.%M')
        debug_backup_sub = self.config.path_debug_backup / backup_dt

        dfl = [dfl for dfl in self.config.path_debug.iterdir() if dfl.stem != 'backup']

        if len(dfl) == 0:
            if not self.config.path_debug_backup.exists():
                log.debug('Debug backup path does not exist. Creating.')
                self.config.path_debug_backup.mkdir(mode=0o770)
        elif len(dfl) >= 1:
            log.debug('Previous debug content found. Moving to: {}'.format(debug_backup_sub))
            debug_backup_sub.mkdir(mode=0o770, parents=True)
            for fof in dfl:
                move(fof.as_posix(), debug_backup_sub.as_posix())

    def debug(self, source, data):

        if self.config.debug:
            path = self.config.path_debug_core
            if not path.exists():
                path.mkdir(mode=0o770, parents=True)
            timestamp = datetime.now().strftime('%Y-%m-%d - %H:%M:%S')
            if source == 'update':
                update_path = path / source
                with update_path.open('a+') as f:
                    f.write('{}\n'.format(data))

    def update(self):

        raw_data = self.browser.update()
        if raw_data:
            self.debug('update', raw_data)
            raw_data = raw_data.decode('utf-8')
            if any(['DOCTYPE' in raw_data, raw_data == None]):
                log.debug('Request error. Ignoring.')
            elif all([isinstance(raw_data, str), raw_data.startswith(')]}\'\n[[[[')]):
                raw_data = raw_data.split('[[')[2:]
                self.people = self.location.update(raw_data)
        else:
            log.error('Update failed.')
