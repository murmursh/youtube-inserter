from browser_mod.mytypes import Simple_Task
from selenium.webdriver.common.by import By
from browser_mod.browser import Browser
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test_task_Browser(Browser):

    def run_task(self, task:Simple_Task, new_page=True):
        if new_page:
            task.window = self.open_new_page()
        else:
            task.window = self.get_current_window()
        self.driver.get(task.get_url())

    def wait_for_task(self, task:Simple_Task):
        if not task.wait_for_it():
            return

        self.select_window(task.window)
        by, query = task.wait_for_it()
        try:
            element = WebDriverWait(self.driver, task.wait_timeout()).until(
                EC.presence_of_element_located((by, query))
            )
        except Exception as ex:
            # print(ex)
            # print("probably fail")
            return

    def validate_task(self, task:Simple_Task):
        if not task.validate_by_this():
            return False
        self.select_window(task.window)
        by, query = task.validate_by_this()
        try:
            element = self.driver.find_element(by=by, value=query)
            return element.text
        except Exception as ex:
            # print(ex)
            # print("probably fail")
            return False
    
    def screenshot_task(self, task:Simple_Task):
        self.select_window(task.window)
        name = type(task).__name__
        path = f"{name}.png"
        self.save_fullscreen_screenshot(path=r'.', name=path)

    def bot_check(self, task_list:list[Simple_Task]):
        for task in task_list:
            self.run_task(task=task)
        for task in task_list:
            self.wait_for_task(task=task)
        for task in task_list:
            val_res = self.validate_task(task=task)
            print(f"task: {task.get_url()} - {val_res}")
            self.screenshot_task(task=task)

class Pixel_scan(Simple_Task):
    def get_url(self):
        return "https://pixelscan.net/"
    
    def wait_timeout(self):
        return 180
    
    def wait_for_it(self):
        return (By.XPATH, "/html/body/pxlscn-root/pxlscn-scanner/div/main/div/pxlscn-home/div/section[1]/pxlscn-consistency-check/div[1]/h1/span")
    
    def validate_by_this(self):
        return self.wait_for_it()
    
class Sany_soft(Simple_Task):
    def get_url(self):
        return "https://bot.sannysoft.com/"
    
    def wait_for_it(self):
        return (By.XPATH, '//*[@id="broken-image-dimensions"]')


class Nowsec_check(Simple_Task):
    def __init__(self) -> None:
        pass

    def get_url(self):
        return "https://nowsecure.nl/"
    

    def validate_by_this(self):
        return By.XPATH, "/html/body/div[2]/div/main/p[2]/a"
