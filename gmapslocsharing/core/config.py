from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path as p
import logging
import ast

log = logging.getLogger(__name__)

class Config:

    class __Config:

        def __init__(self, config_path, debug):

            log.debug('Initializing Config module.')
            self.path = config_path
            self.debug = debug
            self.config = ConfigParser(interpolation=ExtendedInterpolation())
            self.startup()

        def startup(self):

            config =    [
                        path for path in \
                        (self.path / 'deps/lib').glob('python*')
                        ][0] \
                        / 'site-packages/gmapslocsharing/core/config.conf'
            self.config.read(config)

        def get(self, section:str, key:str):
            """
            input: section, key
            """
        def get(self, section:str, key:str):
            """
            input: section, key
            """
            try:
                try:
                    return ast.literal_eval(self.config.get(section, key))
                except:
                    log.warning('Unable to return literal eval for {}.{}.'.format(section, key))
                try:
                    return self.config.get(section, key)
                except:
                    log.error('Standard return for {}.{} also failed.'.format(section, key))
            except Exception as e:
                log.error('Config get error: {}'.format(e))

        def set(self, section:str, key:str, value):
            """
            input: section, key, value
            """

            if not self.config.has_section(section):
                self.config.add_section(section)

            self.config.set(section, key, value)

        @property
        def email(self):
            return self.get('account', 'email')

        @property
        def password(self):
            return self.get('account', 'password')

        @property
        def path_chrome(self):
            return self.path / 'chrome'

        @property
        def path_debug(self):
            return self.path / 'debug'

        @property
        def path_debug_core(self):
            return self.path / 'debug/core'

        @property
        def path_debug_browser(self):
            return self.path / 'debug/browser'

        @property
        def path_debug_location(self):
            return self.path / 'debug/location'

        @property
        def path_debug_backup(self):
            return self.path / 'debug/backup'

        @property
        def path_chrome_nuke(self):
            chrome_cookie_paths = self.get('paths', 'chrome_cookies')
            chrome_cache_paths = self.get('paths', 'chrome_cache')
            return [self.path / path for path in (chrome_cookie_paths + chrome_cache_paths)]

        @property
        def requests_get(self):
            return self.get('requests', 'get')

        @property
        def requests_path(self):
            return self.get('requests', 'path')

        @property
        def login_start(self):
            return self.get('urls', 'login_start')

        @property
        def login_success(self):
            return self.get('urls', 'login_success')

        @property
        def cookie_check(self):
            return self.get('urls', 'cookie_check')

    instance = None

    def __init__(self, config_path=None, debug=False):

        if not Config.instance:
            Config.instance = Config.__Config(config_path, debug)
            Config.instance.startup()

    def __getattr__(self, name):

        return getattr(self.instance, name)
