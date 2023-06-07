import platform
import shutil
import subprocess
import sys
import io
import zipfile
import os
#import undetected_chromedriver._compat as uc

from random import choice

from undetected_chromedriver.patcher import Patcher

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        WebDriverException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CHROME = ['{8A69D345-D564-463c-AFF1-A69D9E530F96}',
          '{8237E44A-0054-442C-B6B6-EA0509993955}',
          '{401C381F-E0DE-4B85-8BD8-3F3F14FBDA57}',
          '{4ea16ac7-fd5a-47c3-875b-dbf4a2008c20}']

EXTENTIONS = os.path.abspath(path="./extentions")

#possible gpus
GPUS = [
    'ANGLE (AMD Radeon R9 M200X Series Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon R9 M200X Series Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon(TM) R7 Graphics Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon(TM) R7 Graphics Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon(TM) R7 Graphics Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon(TM) R9 380 Series Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon(TM) R9 380 Series Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon(TM) R9 390 Series Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon(TM) R9 390 Series Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon(TM) R9 390X Series Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon(TM) R9 390X Series Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon(TM) R9 M275X Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (AMD Radeon(TM) R9 M275X Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 1070 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 1080 Ti Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 1650 SUPER Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 1660 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 1660 SUPER Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 1660 Ti with Max-Q Design Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 750 Ti Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 970 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX 980 Ti Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce GTX TITAN X Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce MX130 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (NVIDIA GeForce MX250 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon (TM) RX 480 Graphics Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon (TM) RX 570 Graphics Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon (TM) RX 6700 XT Graphics Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon (TM) RX Vega Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon (TM) RX Vega M GL Graphics Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon (TM) RX Vega M Graphics Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon (TM) RX Vega64 Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon(TM) RX 460 Graphics Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon(TM) RX 560 Series Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon(TM) RX 580 Series Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon(TM) RX 590 Series Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon(TM) RX 6800 XT Graphics Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon(TM) RX 6800 Graphics Direct3D11 vs_5_0 ps_5_0)',
    'ANGLE (Radeon(TM) RX 6900 XT Graphics Direct3D11 vs_5_0 ps_5_0)',
]

SHADING_LANGUAGE_VERSION = [
    "WebGL GLSL ES 2.0 (OpenGL ES GLSL ES 2.0 Chromium)",
    "WebGL GLSL ES 3.0 (OpenGL ES GLSL ES 3.0 Chromium)"
]
VERSION = [
    "WebGL 1.0 (OpenGL ES 2.0)",
    "WebGL 1.0 (OpenGL ES 3.0)",
    "WebGL 2.0 (OpenGL ES 3.0)"
]


def get_shading_language_version(version):
    """
    Returns the shading language version for a given WebGL or OpenGL version string.

    Args:
        version (str): The WebGL or OpenGL version string, e.g. 'WebGL 2.0' or 'OpenGL ES 3.1'.

    Returns:
        str: The corresponding shading language version, e.g. 'WebGL GLSL ES 3.0' or 'OpenGL GLSL ES 3.1'.
    """
    if 'WebGL' in version:
        if '2.0' in version:
            return 'WebGL GLSL ES 3.0'
        elif '1.' in version:
            return 'WebGL GLSL ES 1.0'
        else:
            return None
    elif 'OpenGL ES' in version:
        if '3.2' in version:
            return 'OpenGL GLSL ES 3.2'
        elif '3.1' in version:
            return 'OpenGL GLSL ES 3.1'
        elif '3.0' in version:
            return 'OpenGL GLSL ES 3.0'
        else:
            return None
    else:
        return None


def get_webgl_renderer(unmasked_renderer_webgl):
    gpu_map = {
        "Intel": "Intel HD Graphics",
        "AMD": "AMD Radeon",
        "Radeon": "AMD Radeon",
        "ATI": "AMD Radeon",
        "NVIDIA": "NVIDIA GeForce",
        "Mali": "Mali",
        "PowerVR": "PowerVR",
        "Adreno": "Adreno",
        "Vivante": "Vivante",
        "Broadcom": "Broadcom"
    }
    for gpu_name in gpu_map.keys():
        if gpu_name in unmasked_renderer_webgl:
            return gpu_map[gpu_name]
    return "Unknown"

def get_vendor(unmasked_renderer_webgl):
    vendors = {
        "Intel": "Google Inc. (Intel)",
        "NVIDIA": "Google Inc. (NVIDIA)",
        "AMD": "Google Inc. (AMD)",
        "Radeon": "Google Inc. (AMD)",
    }
    for vendor in vendors:
        if vendor in unmasked_renderer_webgl:
            return vendors[vendor]

    return 'Intel Inc.'


def get_webgl_vendor(unmasked_renderer_webgl):
    vendors = {
        'Intel': 'Intel Inc.',
        'NVIDIA': 'NVIDIA Corporation',
        'Qualcomm': 'Qualcomm',
        'ATI': 'Advanced Micro Devices, Inc.',
        'AMD': 'Advanced Micro Devices, Inc.',
        'WebKit': 'WebKit',
        'ANGLE': 'Google Inc.',
        'Mesa': 'Brian Paul',
        'SwiftShader': 'Google Inc.',
        'Microsoft': 'Microsoft Corporation',
        'Imagination': 'Imagination Technologies',
        'ARM': 'ARM',
        'Apple': 'Apple Inc.'
    }
    
    for vendor in vendors:
        if vendor in unmasked_renderer_webgl:
            return vendors[vendor]

    return 'Google Inc.'

# depricated
# def download_driver(patched_drivers):
#     osname = platform.system()
#     if osname == 'Linux':
#         osname = 'lin'
#         exe_name = ""
#         with subprocess.Popen(['google-chrome-stable', '--version'], stdout=subprocess.PIPE) as proc:
#             version = proc.stdout.read().decode('utf-8').replace('Google Chrome', '').strip()
#     elif osname == 'Darwin':
#         osname = 'mac'
#         exe_name = ""
#         process = subprocess.Popen(
#             ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
#         version = process.communicate()[0].decode(
#             'UTF-8').replace('Google Chrome', '').strip()
#     elif osname == 'Windows':
#         osname = 'win'
#         exe_name = ".exe"
#         version = None
#         try:
#             process = subprocess.Popen(
#                 ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
#                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
#             )
#             version = process.communicate()[0].decode(
#                 'UTF-8').strip().split()[-1]
#         except Exception:
#             for i in CHROME:
#                 for j in ['opv', 'pv']:
#                     try:
#                         command = [
#                             'reg', 'query', f'HKEY_LOCAL_MACHINE\\Software\\Google\\Update\\Clients\\{i}', '/v', f'{j}', '/reg:32']
#                         process = subprocess.Popen(
#                             command,
#                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
#                         )
#                         version = process.communicate()[0].decode(
#                             'UTF-8').strip().split()[-1]
#                     except Exception:
#                         pass

#         if not version:
#             print("Couldn't find your Google Chrome version automatically!")
#             version = input('Please input your google chrome version (ex: 91.0.4472.114) : ')
#     else:
#         input('{} OS is not supported.'.format(osname))
#         sys.exit()

#     try:
#         with open('version.txt', 'r') as f:
#             previous_version = f.read()
#     except Exception:
#         previous_version = '0'

#     with open('version.txt', 'w') as f:
#         f.write(version)

#     if version != previous_version:
#         try:
#             os.remove(f'chromedriver{exe_name}')
#         except Exception:
#             pass

#         shutil.rmtree(patched_drivers, ignore_errors=True)

#     major_version = version.split('.')[0]

#     uc.TARGET_VERSION = major_version

#     uc.install()

#     return osname, exe_name

def list_files(folder_path):
    """
    Returns a list of file names in a specified folder.

    Args:
        folder_path (str): The path to the folder to list files in.

    Returns:
        List[str]: A list of file names in the folder.
    """
    files = []
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def file_exists(file_path):
    """
    Checks if a file exists at the specified path.

    Args:
        file_path (str): The path to the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(file_path)

def copy_drivers(cwd, patched_drivers, exe, total):
    current = os.path.join(cwd, f'chromedriver{exe}')
    os.makedirs(patched_drivers, exist_ok=True)

    for i in range(total+1):
        try:
            destination = os.path.join(
                patched_drivers, f'chromedriver_{i}{exe}')
            shutil.copy(current, destination)
        except Exception:
            pass

def get_patched_driver() -> webdriver.Chrome:

    osname, exe_name = download_driver(patched_drivers=patched_drivers)
    copy_drivers(cwd=cwd, patched_drivers=patched_drivers,
                        exe=exe_name, total=1)
    patched_driver = os.path.join(
                patched_drivers, f'chromedriver_{1}{exe_name}')
    Patcher(executable_path=patched_driver).patch_exe()

    return get_driver(patched_driver)

def build_all_folders(path):
    
    for foldername, subfolders, filenames in os.walk(path):
        for subfolder in subfolders:
            folderpath = os.path.join(foldername, subfolder)
            zippath = folderpath + '.zip'
            with zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folderpath):
                    for file in files:
                        filepath = os.path.join(root, file)
                        zipf.write(filepath, os.path.relpath(filepath, folderpath))

def get_extentions(path):
    build_all_folders(path=path)
    zip_files = []
    for file in os.listdir(path):
        if file.endswith('.zip'):
            zip_files.append(os.path.join(path, file))
    return zip_files

# add proxys, viewports
def get_driver(path, background=False, agent = None, auth_required=None, viewports=None, proxy=None, proxy_type=None, proxy_folder=None, browser_session = None):
    options = webdriver.ChromeOptions()
    options.headless = background
    if viewports:
        options.add_argument(f"--window-size={choice(viewports)}")
    options.add_argument("--log-level=3")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    prefs = {"intl.accept_languages": 'en_US,en',
             "credentials_enable_service": False,
             "profile.password_manager_enabled": False,
             "profile.default_content_setting_values.notifications": 2,
             "download_restrictions": 3}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('extensionLoadTimeout', 120000)
    if agent:
        options.add_argument(f"user-agent={agent}")
    options.add_argument("--mute-audio")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-features=UserAgentClientHint')
    options.add_argument("--disable-web-security")
    webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {
        'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

    for ext in get_extentions(EXTENTIONS):
        options.add_extension(ext)
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

    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service, options=options)

    return driver

