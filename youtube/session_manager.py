from browser_mod import BrowserSession
from pathlib import Path

class SessionManager:
    def __init__(self):
        self.youtube_fix = Path("extentions/1.4_0")
        self.create_test_session()
        
    def create_test_session(self):
        self.test_session = BrowserSession(name="test", overwrite=True)
        self.test_session.add_extention(self.youtube_fix)
        
    def get_test_session(self):
        return self.test_session