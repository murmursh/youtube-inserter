from browser_mod import Browser
from browser_mod.mytypes import BrowserSessionType
from browser_mod.browser import By



"""
The system state concept:

We have a system that can break randomly and we have no control over when or how it breaks.

To manage this, we define possible states of the system (for example, a URL).

When we encounter an error (for example, a button is missing that is needed for a particular task), the system will transition to an "error" state.

The system will then try to return itself to the correct state needed to perform the task. This may involve reloading the URL, clearing caches, restarting components, etc.

By defining system states and transitions between those states, we can build logic to recover from issues and get the system back to a working condition.
"""
class YoutubeBrowser(Browser):
    def __init__(self, ses:BrowserSessionType, login:str, password:str, chanel_name:str) -> None:
        self.login = login
        self.password = password
        self.chanel_name = chanel_name
        self.load_driver(ses)
        if not self.test_auth():
            self.auth()
        

    def select_chanel(self):
        self.open_url("https://www.youtube.com/channel_switcher")
        chanels = self.wait_and_get_all(By.ID, 'channel-title', timeout = 20)
        if chanels:
            for chanel in chanels:
                if chanel.text == self.chanel_name:
                    self.click(chanel)
                    return
            self.logger.error("No chanel found")
        else:
            self.logger.error("No chanels found")


    def test_auth(self):
        self.open_url("https://www.youtube.com/channel_switcher")
        email = self.get_and_return(By.XPATH, '//*[@id="identifierId"]')
        if email:
            return False
        password = self.get_and_return(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
        if password:
            return False
        return True        

    def auth(self):
        self.open_url("https://www.youtube.com/channel_switcher")
        email = self.get_and_return(By.XPATH, '//*[@id="identifierId"]')
        if email:
            email.send_keys(self.login)
            next_btn = self.get_and_return(By.XPATH, '//*[@id="identifierNext"]')
            self.click(next_btn)
        password = self.wait_and_get(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input', timeout=10)
        if password:
            password.send_keys(self.password)
            next_btn = self.get_and_return(By.XPATH, '//*[@id="passwordNext"]')
            self.click(next_btn)
        self.select_chanel()
        
    def view_video(self, url:str, start:int, end:int, like = False, dislike=False, comment=""):
        """
        url: video url,
        start: start time,
        end: end time,
        like: like video,
        dislike: dislike video,
        comment: comment on video,
        """
        self.open_url(url)
        