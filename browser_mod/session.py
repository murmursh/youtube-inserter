# Import necessary modules
import logging
import os
from selenium import webdriver
from browser_mod.chrome_driver_shinanigans import GPUS, VERSION, get_webgl_vendor, get_shading_language_version, get_webgl_renderer, get_vendor
from random import choice
from browser_mod.utls import get_extentions, get_folder_names, get_minimal_string, is_folder_exists,\
                             backup_rename_folder, create_folder, setup_logger,\
                             get_platform_info, check_file_exists, get_last_webdriver,\
                             process_and_copy_driver, get_driver
from browser_mod.safe_json_objs import JsonSafeDictMethod
from browser_mod.extentions import antifingerprint_extention
from threading import RLock
from browser_mod.mytypes import BrowserSessionType, BrowserType, TabClosedException



# Define a class for managing browser sessions
class BrowserSession(JsonSafeDictMethod, BrowserSessionType):

    """
    Class for managing browser sessions.

    It loads or creates sessions folder in session path that contains browser binary,
    config file, extensions, and browser user data such as cookies. The object stores fake
    hardware and software values.
    """
    def __init__(self, name:str = None, session_path:str = None, sessions_path:str = "./sessions", gpu:str = None, version:str = None, overwrite:bool = False, platform:dict = None) -> None:
        """
        Initialize a new instance of BrowserSession class.

        Args:
            name (str): A string representing the name of the session (optional).
            session_path (str): A string representing the path of the session (optional).
            sessions_path (str):  A string representing the path of the sessions folder (optional).
            gpu (str): A string representing the GPU to use (optional).
            version (str): A string representing the version to use (optional).
            override (bool): A boolean flag indicating whether to override existing session (optional).
        """
        self.lock = RLock()

        # Set instance variables
        self.sessions_path = os.path.abspath(path=sessions_path)
        self.logging_path = os.path.join(self.sessions_path, "log.log")
        self.logger:logging.Logger = None
        
        self.name = name
        self.driver = None
        self.update_logger()

        self._override = overwrite
        self._platform = platform
        self.gpu = gpu 
        self.session_path = session_path
        self.version = version

        self._is_valid = self._load_data()
        self.logging_path = os.path.join(self.session_path, "log.log")
        self.update_logger()

        self._browsers:list[BrowserType] = []

    def update_logger(self):
        new_log_name = f"session_{self.name if self.name else 'init'}"
        if self.logger:
            self.logger.debug(f"New logger - {new_log_name} path - {self.logging_path}")
        self.logger = setup_logger(name=new_log_name, log_file=self.logging_path)


    def _put_default_if_needed(self) -> None:
        self.logger.info("Checking if defaults need to be set")
        if not self.gpu:
            self.gpu = choice(GPUS)
            self.logger.info(f"Set GPU to {self.gpu}")
        if not self.version:
            self.version = choice(VERSION)
            self.logger.info(f"Set version to {self.version}")
        if not self._platform:
            self._platform = get_platform_info()
            self.logger.info(f"Set platform to {self._platform}")

    def _add_browser(self, br:BrowserType) -> None:
        self.logger.info("Adding Browser")
        self._browsers.append(br)


    def _load_data(self) -> None:
        """
        Load data for the current instance of BrowserSession class.

        This method tries to restore an existing session by name or session folder. If none
        found or override flag is set, it creates a new session and generates fake hardware
        and software values for it.
        """
        self.logger.info("Loading data for BrowserSession instance")
        # If not overriding, try to restore session by name or session folder
        self._put_default_if_needed()
        if not self._override:
            if self._try_to_restore():
                self.logger.info("Restored existing session")
                return True
            else:
                self.logger.info("No existing session found")
                return False
            
        # Create a new session
        self._create_session()
        self.logger.info("Created new session")
        return True


    def _try_to_restore_by_name(self) -> bool:
        """
        Try to restore an existing session by name.

        Returns:
            True if a valid session was found and restored, False otherwise.
        """
        self.logger.info("Trying to restore existing session by name")
        # generating session path and restoring by it
        self._generate_new_session_path()
        restored = self._try_to_restore_by_session()
        if restored:
            self.logger.info("Restored session by name")
        else:
            self.logger.info("No session found by name")
        return restored
    
    def _try_to_restore_by_session(self) -> bool:
        """
        Try to restore an existing session by session folder.

        Returns:
            True if a valid session was found and restored, False otherwise.
        """
        self.logger.info("Trying to restore existing session by session folder")
        try:
            self._from_json_file(os.path.join(self.session_path, "session_config.json"))
            self.logger.info("Restored session by session folder")
            return True
        except Exception as ex:
            self.logger.info("No session found by session folder")
            return False


    def _try_to_restore(self) -> None:
        """
        Try to restore an existing session.
        self.name should match with session path otherwise it will use name and overwrite session path

        Returns:
            True if a valid session was found and restored, False otherwise.
        """
        self.logger.info("Trying to restore existing session")
        # Try to restore by name or session folder
        if self.name:
            if self._try_to_restore_by_name():
                return True
        if self.session_path:
            if self._try_to_restore_by_session():
                return True
        self.logger.info("No existing session found")
        return False


    def _create_session(self) -> None:
        """
        Create a new session.

        This method gets a new folder, copies a new webdriver instance to the folder,
        sets up necessary files and folders for the session, and sets the current session
        as the active session.
        """
        self.logger.info("Creating new session")
        # Generate new name if it does not specified
        if not self.name:
            self.logger.info("Generating new name for session")
            self._generate_new_name()

        if not self.session_path:
            self.logger.info("Generating new session path")
            self._generate_new_session_path()

    
    def _generate_new_session_path(self) -> None:
        self.logger.info("Generating new session path")
        self.session_path = os.path.join(self.sessions_path, f"session_{self.name}")
        if self._override:
            self.logger.info("Backing up existing session folder")
            backup_rename_folder(self.session_path)
        create_folder(self.sessions_path, f"session_{self.name}")
        create_folder(self.session_path, f"extensions")
        create_folder(self.session_path, f"user-data")
        self.logger.info("Putting new data for session")
        self._put_new_data()
        

    def _put_new_data(self):
        self.to_json_file(os.path.join(self.session_path, "session_config.json"))


    def _generate_new_name(self) -> None:
        """
        Generate a new name.

        This method generates a new unique name based on the sessions path.
        """
        self.logger.info("Generating new name for session")

        # Get the names of all folders in the sessions path.
        folders = get_folder_names(self.sessions_path)

        # Create an empty list to store the extracted names.
        names = []

        # Extract the name from each folder that starts with "session_".
        for folder in folders:
            if folder.startswith("session_"):
                names.append(folder.removeprefix("session_"))

        # Get the minimal string from the extracted names and set it as the new name.
        self.name = get_minimal_string(names)
        self.logger.info(f"New session name generated: {self.name}")

    def _set_aditional_values(self):
        self._webgl_renderer = get_webgl_renderer(self.gpu)
        self._webgl_vendor = get_webgl_vendor(self.gpu)
        self._unmasked_vendor_webgl = get_vendor(self.gpu)
        self._shading = get_shading_language_version(self.version)

    def get_data(self):
        self._set_aditional_values()
        data = self.__safe_dict__()
        data.update({"webgl_renderer": self._webgl_renderer, 'webgl_vendor': self._webgl_vendor, "unmasked_vendor_webgl":self._unmasked_vendor_webgl, 'shading': self._shading})
        return data

    def _build_extentions(self):
        self._set_aditional_values()
        self.logger.info(f"Additional values: WebGL renderer: {self._webgl_renderer}, WebGL vendor: {self._webgl_vendor}, Shading language version: {self._shading}")
        antifingerprint_extention(version=self.version, 
                                vendor=self._webgl_vendor, 
                                unmask_vendor_webgl=self._unmasked_vendor_webgl, 
                                renderer=self._webgl_renderer, 
                                unmasked_renderer_webgl=self.gpu, 
                                shading_language_version=self._shading,
                                move_to=os.path.join(self.session_path, "extensions"))

    def _get_web_driver(self):
        #check for web driver, if missing - copy
        driver_path = os.path.join(self.session_path, f"chrome_driver{self._platform['exe_name']}")
        get_last_webdriver(self._platform['version'])
        if check_file_exists(driver_path):
            return
        # copy new chrome_driver 

        process_and_copy_driver(self.session_path, f"chromedriver{self._platform['exe_name']}", self._platform['exe_name'])

    def _launch_webdriver(self) -> webdriver.Chrome:
        return get_driver(path = os.path.join(self.session_path, f"chrome_driver{self._platform['exe_name']}"), extentions=get_extentions(os.path.join(self.session_path, "extensions")), user_data=os.path.join(self.session_path, "user-data"))

    def get_driver(self) -> webdriver.Chrome:
        """
        Get a webdriver instance for the current session.

        Returns:
            A new instance of the Chrome webdriver with the configured session options
        """
        if self.driver:
            return self.driver
        self.logger.info("Getting new driver")
        # build extentions with data
        self._build_extentions()
        # get chromedriver if needed
        #self._get_web_driver()
        # launch it with parms
        self.driver = self._launch_webdriver()
        return self.driver
    
    def stop_session(self):
        for br in self._browsers:
            try:
                br.stop_browser()
            except TabClosedException as e:
                pass
    
        if self.driver:
            self.driver.quit()
            del self.driver
            self.driver = None

        for br in self._browsers:
            br.join()


    def delete(self):
        backup_rename_folder(self.session_path)




def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')
    s = BrowserSession(name="q")
    s.get_driver()


if __name__ == "__main__":
    main()