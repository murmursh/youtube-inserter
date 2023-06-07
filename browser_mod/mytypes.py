
from selenium.webdriver.common.by import By
from typing import List

class Simple_Task:
    window = None
    def __init__(self, url=None) -> None:
        self.url = url

    def wait_timeout(self):
        return 20

    def get_url(self):
        return self.url
    
    def wait_for_it(self):
        return None
    
    def validate_by_this(self):
        return None
    
class Window:
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name
    
class BrowserSessionType:
    lock = None
    sessions_path = None
    logging_path = None
    logger = None
    name = None
    driver = None
    gpu = None
    version = None

    def get_driver(self):
        ...

    def stop_session(self):
        ...

    def delete(self):
        ...

    def get_data(self):
        ...
    
class BrowserType:
    session = None
    lock = None
    driver = None
    logger = None
    window = None


    def load_driver(self, session:BrowserSessionType):
        ...

    def get_current_window(self):
        ...

    def stop_browser(self):
        ...

    def open_url(self, url:str) -> bool:
        ...
    
    def get_and_return(self, by, value):
        ...

    def get_and_click(self, by, value):
        ...

    def click(self, element):
        ...

    def wait_and_get(self, by:By, value:str, timeout:int = 1) -> bool:
        ...
        
    def wait_and_get_all(self, by:By, value:str, timeout:int = 1) -> bool:
        ...

    def get_all(self, by:By, value:str) -> bool:
        ...

    def wait_and_click(self, by:By, value:str, timeout:int = 1) -> bool:
        ...

    def open_new_page(self) -> Window:
        ...

    def select_window(self, window:Window) -> None:
        ...

    def save_fullscreen_screenshot(self, path: str = '/tmp/', name = "lol.png") -> str:
        ...

    def safe_executer(self, func, *args, **kwargs):
        ...
    
    def execute_script(self, scrpt):
        ...
    
    def wait(self, time):
        ...

class TabClosedException(Exception):
    ...