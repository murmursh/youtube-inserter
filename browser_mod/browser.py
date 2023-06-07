import random

from browser_mod.chrome_driver_shinanigans import get_patched_driver
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser_mod.utls import Screenshot
from typing import Union
from browser_mod.mytypes import Window, BrowserSessionType, BrowserType, TabClosedException
    
def Browser_spec(func):
    def wrapper(self, *args, **kwargs):
        with self.lock:
            if self.window:
                try:
                    self._select_window(self.window)
                except WebDriverException:
                    raise TabClosedException("Tab closed")
            return func(self, *args, **kwargs)
    return wrapper

class Browser(BrowserType):
    '''
    Mixin class for driver usage
    '''

    def load_driver(self, session:BrowserSessionType):
        self.session = session
        self.session._add_browser(self)
        self.lock = self.session.lock
        self.driver = self.session.get_driver()
        self.logger = self.session.logger
        self.window = None
        self.window = self.open_new_page()
        self.logger.info("Driver loaded successfully")

    def get_current_window(self):
        window = self.driver.current_window_handle
        self.logger.debug("Current window handle: {}".format(window))
        return window

    @Browser_spec
    def _stop_browser(self):
        self.stop_browser()

    def stop_browser(self):
        self._close_tab()
        self.logger.info("Browser stopped")


    #cloasing current window
    @Browser_spec
    def _close_tab(self):
        self.driver.close()

    @Browser_spec
    def open_url(self, url:str) -> bool:
        try:
            self.driver.get(url)
            self.logger.info("Opened URL: {}".format(url))
            return True
        except Exception as ex:
            self.logger.error("Error opening URL: {} - {}".format(url, ex))
            return False
    
    @Browser_spec
    def get_and_return(self, by, value):
        try:
            data = self.driver.find_element(by, value)
            self.logger.debug("Found element with {}={}".format(by, value))
            return data
        except:
            self.logger.error("Failed to find element with {}={}".format(by, value))
            return -1

    @Browser_spec
    def get_and_click(self, by, value):
        try:
            agree = self.driver.find_element(by, value)
            self.click(element=agree)
            self.logger.info("Clicked element with {}={}".format(by, value))
            return True
        except WebDriverException:
            self.logger.warning("Failed to click element with {}={}".format(by, value))
            return False

    @Browser_spec
    def click(self, element):
        self.driver.execute_script(
        "arguments[0].scrollIntoViewIfNeeded();", element)
        sleep(0.5)
        element.click()
        self.logger.debug("Clicked element")

    @Browser_spec
    def wait_and_get(self, by:By, value:str, timeout:int = 1) -> bool:
        try:
            agree = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(
                (by, value)))
            self.logger.info("Waited for element with {}={}".format(by, value))
            
            return agree
        except Exception as ex:
            return False
        
    @Browser_spec
    def wait_and_get_all(self, by:By, value:str, timeout:int = 1) -> bool:
        try:
            agree = WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(
                (by, value)))
            self.logger.info("Waited for element with {}={}".format(by, value))
            
            return agree
        except Exception as ex:
            return False

    @Browser_spec
    def get_all(self, by:By, value:str) -> bool:
        try:
            agree = self.driver.find_elements(by, value)
            self.logger.info("Found all elements with {}={}".format(by, value))
            
            return agree
        except Exception as ex:
            return False

    @Browser_spec
    def wait_and_click(self, by:By, value:str, timeout:int = 1) -> bool:
        try:
            agree = self.wait_and_get(by, value, timeout)
            self.click(element=agree)
            self.logger.info("Clicked element with {}={} after waiting for visibility".format(by, value))
            return True
        except WebDriverException:
            self.logger.warning("Failed to wait for and click element with {}={}".format(by, value))
            return False

    @Browser_spec
    def open_new_page(self) -> Window:
        # todo add script for closing first window
        self.driver.switch_to.new_window()
        self.logger.debug("Opened new window")
        return self.get_current_window()

    @Browser_spec
    def select_window(self, window:Window) -> None:
        self._select_window(window)

    def _select_window(self, window:Window) -> None:
        if self.get_current_window() != window:
            self.driver.switch_to.window(window)
            self.logger.info("Selected window: {}".format(window))

    @Browser_spec
    def save_fullscreen_screenshot(self, path: str = '/tmp/', name = "lol.png") -> str:
        ob=Screenshot()
        return ob.full_Screenshot(self.driver, save_path=path, image_name=name, scroll_speed=0.1)

    @Browser_spec
    def safe_executer(self, func, *args, **kwargs):
        return func(*args, **kwargs)
    
    @Browser_spec
    def execute_script(self, scrpt):
        return self.driver.execute_script(scrpt)
    
    #wait driver for time seconds
    def wait(self, time):
        sleep(time)
        
def test_bot():
    from browser_mod.bot_test_tasks import Nowsec_check, Pixel_scan, Sany_soft, Test_task_Browser
    tasks = [
        Sany_soft()
    ]
    driver = get_patched_driver()
    br = Test_task_Browser(driver=driver)
    br.bot_check(tasks)
    sleep(10000)


def main():
    test_bot()
if __name__ == "__main__":
    main()
