import itertools
import os
import platform
from random import choice
import shutil
import subprocess
import time
import logging
import io

from PIL import Image
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service

import undetected_chromedriver as uc

from undetected_chromedriver.patcher import Patcher



formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s:%(message)s')

CHROME = ['{8A69D345-D564-463c-AFF1-A69D9E530F96}',
          '{8237E44A-0054-442C-B6B6-EA0509993955}',
          '{401C381F-E0DE-4B85-8BD8-3F3F14FBDA57}',
          '{4ea16ac7-fd5a-47c3-875b-dbf4a2008c20}']

logging.basicConfig(format='%(name)s %(asctime)s %(levelname)s:%(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

class Screenshot:
    """
        TEMP FIX for Selenium_Screenshot lib
       #================================================================================================================#
       #                                          Class: Screenshot                                                     #
       #                                    Purpose: Captured full and element screenshot using selenium                #
       #                                    a) Capture full webpage as image                                            #
       #                                    b) Capture element screenshots                                              #
       #================================================================================================================#
    """

    def __init__(self):
        """
        Usage:
            N/A
        Args:
            N/A
        Returns:
            N/A
        Raises:
            N/A
        """
        pass

    @staticmethod
    # Take temporary screenshot of the web page to get the size of the image
    def __get_screen_size(driver: WebDriver) -> dict:
        driver.get_screenshot_as_file('screenshot.png')
        image = Image.open('screenshot.png')
        width, height = image.size

        return {'width': width, 'height': height}

    def full_Screenshot(self, driver: WebDriver, save_path: str = '', image_name: str = 'selenium_full_screenshot.png',
                        elements: list = None, is_load_at_runtime: bool = False, load_wait_time: int = 5, multi_images: bool = False,
                        scroll_speed = 0.2) -> str:
        """
        Take full screenshot of web page
        Args:
            driver: The Selenium web driver object
            save_path: The path where to store screenshot
            image_name: The name of screenshot image
            elements: List of Xpath of elements to hide from web pages
            is_load_at_runtime: Page Load at runtime
            load_wait_time: The Wait time while loading full screen
            multi_images: The flag is uses to capture multiple images and create single image in vertical format

        Returns:
            str : The path of image
        """
        image_name = os.path.abspath(save_path + '/' + image_name)

        final_page_height = 0
        original_size = driver.get_window_size()

        if is_load_at_runtime:
            while True:
                page_height = driver.execute_script("return document.body.scrollHeight")
                if page_height != final_page_height and final_page_height <= 10000:
                    driver.execute_script("window.scrollTo(0, {})".format(page_height))
                    time.sleep(load_wait_time)
                    final_page_height = page_height
                else:
                    break

        if isinstance(driver, webdriver.Ie):
            self.hide_elements(driver, elements)
            required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            driver.set_window_size(required_width, final_page_height)
            driver.save_screenshot(image_name)
            driver.set_window_size(original_size['width'], original_size['height'])
            return image_name

        else:
            total_width = driver.execute_script("return document.body.offsetWidth")
            total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
            viewport_width = driver.execute_script("return document.body.clientWidth")
            viewport_height = driver.execute_script("return window.innerHeight")
            driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(scroll_speed*2)
            rectangles = []

            i = 0
            while i < total_height:
                ii = 0
                top_height = i + viewport_height
                if top_height > total_height:
                    top_height = total_height
                while ii < total_width:
                    top_width = ii + viewport_width
                    if top_width > total_width:
                        top_width = total_width
                    rectangles.append((ii, i, top_width, top_height))
                    ii = ii + viewport_width
                i = i + viewport_height
            stitched_image = None
            previous = None
            part = 0

            stitched_image = Image.new('RGB', (total_width, total_height))
            height_remaining = total_height
            

            for rectangle in rectangles:
                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                time.sleep(scroll_speed)
                self.hide_elements(driver, elements)

                file_name = "part_{0}.png".format(part)
                driver.get_screenshot_as_file(file_name)
                screenshot = Image.open(file_name)
                if screenshot.height > height_remaining:
                    screenshot = screenshot.crop((0, screenshot.height - height_remaining, screenshot.width, screenshot.height))

                offset = (rectangle[0], rectangle[1])

                stitched_image.paste(screenshot, offset)
                height_remaining = height_remaining - screenshot.height
                del screenshot
                os.remove(file_name)
                part = part + 1
            save_path = os.path.abspath(os.path.join(save_path, image_name))
            stitched_image.save(save_path)
            return save_path

    def get_element(self, driver: WebDriver, element: WebElement, save_location: str, image_name: str = 'cropped_screenshot.png', to_hide: list = None) -> str:
        """
         Usage:
             Capture Element screenshot as a image
         Args:
             driver: Web driver instance
             element : The element on web page to be captured
             save_location  : Path where to save image
         Returns:
             img_url(str) : The path of image
         Raises:
             N/A
         """
        image = self.full_Screenshot(driver, save_path=save_location, image_name='clipping_shot.png', elements=to_hide, multi_images=True)
        location = element.location
        size = element.size
        x = location['x']
        y = location['y']
        w = size['width']
        h = size['height']
        width = x + w
        height = y + h

        image_object = Image.open(image)
        image_object = image_object.crop((int(x), int(y), int(width), int(height)))
        img_url = os.path.abspath(os.path.join(save_location, f"{image_name}.png"))
        image_object.save(img_url)
        return img_url

    @staticmethod
    def hide_elements(driver: WebDriver, elements: list) -> None:
        """
         Usage:
             Hide elements from web page
         Args:
             driver : The path of chromedriver
             elements : The element on web page to be hide
         Returns:
             N/A
         Raises:
             N/A
         """
        if elements is not None:
            try:
                for e in elements:
                    sp_xpath = e.split('=')
                    if 'id=' in e.lower():
                        driver.execute_script(
                            "document.getElementById('{}').setAttribute('style', 'display:none;');".format(
                                sp_xpath[1]))
                    elif 'class=' in e.lower():
                        driver.execute_script(
                            "document.getElementsByClassName('{}')[0].setAttribute('style', 'display:none;');".format(
                                sp_xpath[1]))
                    else:
                        print('For Hiding Element works with ID and Class Selector only')
            except Exception as Error:
                print('Error : ', str(Error))

def backup_rename_folder(path: str) -> bool:
    """
    Create a backup copy of a folder at the specified path, appending '_copy{timestamp}' to its name.

    Args:
        path (str): Path to folder to backup.

    Returns:
        bool: True if backup copy was successfully created, False otherwise.
    """
    if not is_folder_exists(path):
        return False
    
    # Create timestamp for backup copy
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    
    # Create new path with timestamp suffix
    path_copy = f"{path}_copy{timestamp}"
    
    try:
        # Copy original folder to new path
        os.rename(path, path_copy)
        return True
    except Exception as ex:
        return False

def create_folder(path, folder_name):
    # Combine the path and folder name to create the full path to the new folder.
    full_path = os.path.join(path, folder_name)

    # Check if the folder already exists.
    if os.path.exists(full_path):
        return False
    else:
        try:
            # Create the new folder.
            os.mkdir(full_path)
            return True
        except OSError:
            return False

def is_folder_exists(path: str) -> bool:
    """Check if a folder exists at the specified path.

    Args:
        path (str): Path to folder.

    Returns:
        bool: True if folder exists, False otherwise.
    """
    return os.path.isdir(path)

def get_folder_names(path:str) -> list:
    """
    Returns a list of folder names in the given path.
    """
    folder_names = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            folder_names.append(item)
    return folder_names

def get_minimal_string(strings: list) -> str:
    """Returns the minimal string that is not in the given list of strings.
    
    Args:
        strings: A list of strings.
    
    Returns:
        The minimal string that is not in the given list of strings.
    """
    # Create a set of all lowercase letters
    letters = set('abcdefghijklmnopqrstuvwxyz')
    
    # Iterate through all possible lengths of strings
    for length in range(1, len(strings)+2):
        # Iterate through all possible combinations of letters of that length
        for candidate in itertools.product(letters, repeat=length ):
            # Convert candidate to a string
            candidate_str = ''.join(candidate)
            
            # Check if candidate is not in the list of strings
            if candidate_str not in strings:
                return candidate_str
                
    # If all possible strings are in the list of strings, return an empty string
    return ''

def get_platform_info() -> dict:
    # Get the name of the operating system
    osname = platform.system()

    # If the OS is Linux, get the version of Google Chrome
    if osname == 'Linux':
        osname = 'lin'
        exe_name = ""
        with subprocess.Popen(['google-chrome-stable', '--version'], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode('utf-8').replace('Google Chrome', '').strip()

    # If the OS is MacOS, get the version of Google Chrome
    elif osname == 'Darwin':
        osname = 'mac'
        exe_name = ""
        process = subprocess.Popen(
            ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode(
            'UTF-8').replace('Google Chrome', '').strip()

    # If the OS is Windows, get the version of Google Chrome
    elif osname == 'Windows':
        osname = 'win'
        exe_name = ".exe"
        version = None
        try:
            # Try to get the version of Google Chrome using the Windows registry
            process = subprocess.Popen(
                ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
            )
            version = process.communicate()[0].decode(
                'UTF-8').strip().split()[-1]

        except Exception:
            # If the version cannot be found using the above method, try other possible registry keys
            for i in CHROME:
                for j in ['opv', 'pv']:
                    try:
                        command = [
                            'reg', 'query', f'HKEY_LOCAL_MACHINE\\Software\\Google\\Update\\Clients\\{i}', '/v', f'{j}', '/reg:32']
                        process = subprocess.Popen(
                            command,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
                        )
                        version = process.communicate()[0].decode(
                            'UTF-8').strip().split()[-1]
                        if version:
                            break

                    except Exception:
                        pass

        # If the version of Google Chrome still cannot be found, raise an error
        if not version:
            raise ValueError("Couldn't find your Google Chrome")

    # If the OS is not supported, raise an error
    else:
        raise OSError(f'{osname} OS is not supported.')

    # Return the name of the OS, the name of the executable, and the version of Google Chrome
    return {"osname":osname, "exe_name":exe_name, "version":version}

def check_file_exists(file_path):
    return os.path.isfile(file_path)

def get_last_webdriver(version):

    major_version = version.split('.')[0]

    uc.TARGET_VERSION = major_version

    uc.install()

def copy_file(src_file, dest_file):
    shutil.copy(src_file, dest_file)

def process_and_copy_driver(session_path, patched_driver, exe_name):
    def monkey_patch_exe(self):
        linect = 0
        replacement = self.gen_random_cdc()
        replacement = f"  var key = '${replacement.decode()}_';\n".encode()
        with io.open(self.executable_path, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"var key = " in line:
                    fh.seek(-len(line), 1)
                    fh.write(replacement)
                    linect += 1
            return linect


    Patcher.patch_exe = monkey_patch_exe
    Patcher(executable_path=patched_driver).patch_exe()
    copy_file(patched_driver, os.path.join(session_path, f"chrome_driver{exe_name}"))

def get_driver(path, background=False, agent = None, auth_required=None, viewports=None, proxy=None, proxy_type=None, proxy_folder=None, browser_session = None, extentions:list = [], user_data = None):
    options = uc.ChromeOptions()
    # options.headless = background
    # if viewports:
    #     options.add_argument(f"--window-size={choice(viewports)}")
    # options.add_argument("--log-level=3")
    # options.add_experimental_option(
    #     "excludeSwitches", ["enable-automation", "enable-logging"])
    # options.add_experimental_option('useAutomationExtension', False)
    # prefs = {"intl.accept_languages": 'en_US,en',
    #          "credentials_enable_service": False,
    #          "profile.password_manager_enabled": False,
    #          "profile.default_content_setting_values.notifications": 2,
    #          "download_restrictions": 3}
    # options.add_experimental_option("prefs", prefs)
    # options.add_experimental_option('extensionLoadTimeout', 120000)
    if agent:
        options.add_argument(f"user-agent={agent}")
    # options.add_argument("--mute-audio")
    # options.add_argument(f"--user-data-dir={user_data}")
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-features=UserAgentClientHint')
    # options.add_argument("--disable-web-security")
    # webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {
    #     'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

    for ext in extentions:
        options.add_argument(f"--load-extension={ext}")
    # if not background:
    #     options.add_extension(WEBRTC)
    #     options.add_extension(FINGERPRINT)
    #     options.add_extension(ACTIVE)

    #     if CUSTOM_EXTENSIONS:
    #         for extension in CUSTOM_EXTENSIONS:
    #             options.add_extension(extension)

    # if auth_required:
    #     create_proxy_folder(proxy, proxy_folder)
    #     options.add_argument(f"--load-extension={proxy_folder}")
    # else:
    #     options.add_argument(f'--proxy-server={proxy_type}://{proxy}')

    #service = Service(executable_path=path)
    driver = uc.Chrome(options=options, user_data_dir=user_data)

    return driver

def get_extentions(path):
    zip_files = []
    for file in os.listdir(path):
        zip_files.append(os.path.join(path, file))
    return zip_files
