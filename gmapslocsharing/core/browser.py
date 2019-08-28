from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from seleniumwire import webdriver

import chromedriver_binary

from random import randrange
from .config import Config
import logging
import shutil
import sys
import os

log = logging.getLogger(__name__)

selenium_logger = logging.getLogger('seleniumwire')
selenium_logger.setLevel(logging.ERROR)

class Browser:

    def __init__(self):

        log.debug('Initializing Browser module.')
        self.config = Config()
        self.driver = self.browser_init()
        self.cookie_check()

    def browser_init(self):

        L = randrange(668,868,1)
        W = randrange(924,1124,1)

        try:
            log.debug('Setting up webdriver Chrome options.')
            chrome_options = Options()
            prefs = {
                    'DefaultJavaScriptSetting': 2,
                    'DefaultGeolocationSetting': 2,
                    'EnableMediaRouter': False,
                    'PasswordManagerEnabled': False,
                    'PrintingEnabled': False,
                    'CloudPrintProxyEnabled': False,
                    'SafeBrowsingExtendedReportingEnabled': False,
                    'AutofillAddressEnabled': False,
                    'BrowserSignin': 0,
                    'BuiltInDnsClientEnabled': False,
                    'CommandLineFlagSecurityWarningsEnabled': False,
                    'MetricsReportingEnabled': False,
                    'NetworkPredictionOptions': 2,
                    'SavingBrowserHistoryDisabled': True,
                    'SearchSuggestEnabled': False,
                    'SpellCheckServiceEnabled': False,
                    'SyncDisabled': True,
                    'TranslateEnabled': False,
                    'UrlKeyedAnonymizedDataCollectionEnabled': False
                    }
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_argument('--user-data-dir={}'.format(self.config.path_chrome))
            chrome_options.add_argument('--window-size={}x{}'.format(L,W))
            chrome_options.add_argument('--disable-plugin-discovery')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.headless = True
            return webdriver.Chrome(options=chrome_options)
        except Exception as e:
            log.debug('Browser init error: {}.'.format(e))

    def browser_login(self):

        if self.driver == None:
            self.driver = self.browser_init()

        try:
            self.driver.get(self.config.login_start)
        except Exception as e:
            log.error('Error opening login url: {}.'.format(e))

        self.debug('01_login')

        try:
            email = self.driver.find_element_by_css_selector('[type=email]')
            email.send_keys(self.config.email)
            email.send_keys(Keys.RETURN)
        except Exception as e:
            log.error('Error entering email: {}.'.format(e))

        self.debug('02_email')

        try:
            password = self.driver.find_element_by_css_selector('[type=password]')
            password.send_keys(self.config.password)
            password.send_keys(Keys.RETURN)
        except Exception as e:
            log.error('Error entering password: {}.'.format(e))

        self.debug('03_password')

        try:
            wait = WebDriverWait(self.driver, 15, poll_frequency=1)
            wait.until(ec.url_to_be(self.config.login_success))
        except Exception as e:
            log.error('Error during 2FA process: {}.'.format(e))

        self.debug('04_2FA')

    def cookie_check(self):

        self.driver.get(self.config.cookie_check)
        all_cookies = [cookie for cookie in self.driver.get_cookies()]
        all_cookie_names = [cookie['name'] for cookie in all_cookies]
        auth_cookies = [cookie for cookie in self.driver.get_cookies() if cookie['name'] in ['SID', 'HSID']]
        if len(auth_cookies) == 2:
            log.debug('Auth cookies exist. Checking expiry.')
            # TODO: figure out the best way to check for cookie
            # expiry and then nuke cookies & cache and perform login.
        elif all([len(all_cookie_names) == 2, '1P_JAR' in all_cookie_names, 'NID' in all_cookie_names]):
            log.debug('No auth cookies exist. Logging in.')
            self.browser_login()
        else:
            log.debug('Nuking cookies & cache.')
            self.nuke_cookies()
            log.debug('Creating new cookie.')

    def nuke_cookies(self):

        log.debug('Deleting all cookies.')
        self.driver.delete_all_cookies()
        log.debug('Quitting driver.')
        self.driver.quit()
        self.driver = None

        log.debug('Nuking cookies & cache.')
        for target in self.config.path_chrome_nuke:
            if target.is_dir():
                shutil.rmtree(target, ignore_errors=False, onerror=None)
            elif target.is_file():
                os.remove(target)

        log.debug('Reinitializing browser and logging in.')
        self.browser_login()

    def debug(self, step):

        if self.config.debug:

            path = self.config.path_debug_browser

            if not path.exists():
                path.mkdir(mode=0o770, parents=True)

            url = path / 'urls'
            ss = path / 'screenshots'

            with url.open('a+') as f:
                f.write('\n\n{} - {}\n'.format(step, self.driver.current_url))

            if not ss.exists():
                ss.mkdir(mode=0o770, parents=True)
            ss_path = ss / '{}.png'.format(step)
            self.driver.save_screenshot(ss_path.as_posix())

    def update(self):

        log.debug('Querying google maps location sharing data.')
        try:
            del self.driver.requests
            driver_get = '{}={}'.format(self.config.requests_get, self.config.email)
            driver_wait = self.config.requests_path
            self.driver.get(driver_get)
            self.driver.wait_for_request(driver_wait)
            requests = [request for request in self.driver.requests]
            for request in requests:
                if self.config.requests_path in request.path:
                    raw_output = request.response.body
            return raw_output
        except Exception as e:
            log.error('Error acquiring location data: {}.'.format(e))

        return False
