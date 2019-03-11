from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium import webdriver

import chromedriver_binary

import requests
import logging
import pickle
import os

log = logging.getLogger(__name__)

class CookieMonster:

    def __init__(self,  login, password, config, path, cookie, resolution,
                    debug):

        self.login = login
        self.password = password
        self.config = config
        self.path = path
        self.cookie = cookie
        self.session = requests.Session()
        self.resolution = resolution
        self.debug = debug

        self.agent = (  'Mozilla/5.0 (X11; Linux x86_64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/69.0.3497.100 Safari/537.36')
        self.header = { 'User-Agent': self.agent,
                        'Referer': self.config['header_referer']}

        self.session.headers.update(self.header)

        self.browser = None
        self.chrome_options = None

    def file_check(self):

        cookie = self.cookie

        try:
            log.debug('Cookie File Check - Checking if cookie exists.')
            if cookie.exists():
                cookie = cookie.as_posix()
                log.debug('Cookie File Check - Attempting to load cookie from file.')
                with open(cookie, mode='rb') as f:
                    self.session.cookies.update(pickle.load(f))
                return True
            else:
                log.warning('Cookie File Check - Cookie file does not exist.')
        except Exception as e:
            log.debug('Cookie File Check - Failed - {}.'.format(e))

        return False

    def validity_check(self):

        log.debug('Cookie Validity Check - Opening login URL via requests.')
        self.session.get(self.config['login_start'])

        # TODO: along with the key check, maybe check the cookie for expiry as well.
        log.debug('Cookie Validity Check - Validating cookie.')
        for key in self.session.cookies.get_dict(domain=self.config['domain']).keys():
            if key in ['1P_JAR', 'APISID', 'CONSENT', 'HSID', 'NID', 'SAPISID', 'SID', 'SIDCC', 'SSID']:
                # not sure if continue is the best method here.
                continue
            else:
                log.warning('Cookie Validity Check - Failed cookie validation.')
                return False

        log.debug('Cookie Validity Check - Cookie exists and is valid.')
        return True

    def browser_init(self):

        try:
            log.debug('Browser Init - Setting up webdriver Chrome options.')
            self.chrome_options = Options()
            self.chrome_options.add_argument('--window-size={}'.format(self.resolution))
            self.chrome_options.add_argument('--no-sandbox')
            self.chrome_options.add_argument('--disable-dev-shm-usage')
            self.chrome_options.set_headless(headless=True)

            log.debug('Driver - Setting Chrome options.')
            self.browser = webdriver.Chrome(chrome_options=self.chrome_options)

            return True

        except Exception as e:
            log.error('Browser Init - Browser initialization failed.')
            log.error('Browser Init - Exception: {}.'.format(e))

        return False

    def browser_login(self):

        # TODO: check if debug folder exists. create it if it doesn't. if folder
        # exists, clear previous contents so there's no debug redundency from
        # previous attempts.

        debug_folder = self.path / 'debug'
        url_log = debug_folder / 'urls.txt'

        try:
            log.debug('Checking if debug folder exists.')
            if not debug_folder.exists():
                log.debug('Debug folder does not exist, creating.')
                debug_folder.mkdir(mode=0o770, parents=True)
                url_log.touch(mode=0o660)
            else:
                log.debug('Debug folder exists. Clearing previous contents.')
                for file in debug_folder.iterdir():
                    os.remove(file)
                url_log.touch(mode=0o660)

            def debug_output(ss, url):
                self.browser.save_screenshot('{}/{}'.format(debug_folder.as_posix(), ss))
                with open(url_log.as_posix(), mode='a') as url_output:
                    url_output.write('{} URL: {}\n'.format(url, self.browser.current_url))

            log.debug('Login - Opening {}.'.format(self.config['login_start']))
            self.browser.get(self.config['login_start'])

            if self.debug:
                debug_output('gmail_login_01.png', 'Login Screen')

            log.debug('Login - Entering email.')
            email = self.browser.find_element_by_css_selector('[type=email]')
            email.send_keys(self.login)

            if self.debug:
                debug_output('gmail_login_02.png', 'Email Submission')

            log.debug('Login - Submitting email.')
            email.send_keys(Keys.RETURN)

            if self.debug:
                debug_output('gmail_login_03.png', 'Password Screen')

            log.debug('Login - Entering password.')
            password = self.browser.find_element_by_css_selector('[type=password]')
            password.send_keys(self.password)

            if self.debug:
                debug_output('gmail_login_04.png', 'Password Submission')

            log.debug('Login - Submitting password.')
            password.send_keys(Keys.RETURN)

            if self.debug:
                debug_output('gmail_login_05.png', '2FA Wait')

            # TODO: could create a login type tree here based on configuration options
            # passed in via configuration.yaml file (notification, authenticator, etc)
            log.debug('Login - Waiting for user to approve login via phone notification...')
            wait = WebDriverWait(self.browser, 10, poll_frequency=1)
            # TODO: the below should be correct for localities which use .com. if
            # this package gains traction, we can have users set their locality in
            # the configuration.yaml file which will translate that locality to the
            # appropriate dict URL which corresponds to the appropriate successful
            # login URL.
            wait.until(ec.url_to_be(self.config['login_success']))

            if self.debug:
                debug_output('gmail_login_06.png', 'Account Home')

            return True

        except Exception as e:
            log.error('Login - Failed - {}.'.format(e))
            return False

    def export_cookies(self):

        try:
            log.debug('Export - Opening {} via requests'.format(self.config['login_start']))
            self.session.get(self.config['login_start'])

            log.debug('Export - Converting selenium cookies to requests.')
            for cookie in self.browser.get_cookies():
                self.session.cookies.set( version=0,
                                    name=cookie['name'],
                                    value=cookie['value'],
                                    domain=cookie.get('domain', None),
                                    path=cookie.get('path', '/'),
                                    secure=cookie.get('secure', False),
                                    expires=cookie.get('expiry', None),
                                    discard=False)

            log.debug('Export - Exporting CookieJar via pickle binary.')

            with open(self.cookie.as_posix(), mode='wb') as f:
                pickle.dump(self.session.cookies, f)
            self.browser.quit()

            return True

        except:
            log.error('Export - Failed.')

        return False

    def check(self):

        if self.file_check() and self.validity_check():
            return True
        else:
            log.info('Beginning cookie acquisition.')
            log.info('Initiating Chrome WebDriver.')
            if self.browser_init():
                log.info('Initiating Login.')
                if self.browser_login():
                    log.info('Initiating Cookie Export.')
                    self.export_cookies()
                    return True
        return False
