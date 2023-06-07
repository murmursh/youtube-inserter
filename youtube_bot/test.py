from browser_mod import BrowserSession
from browser_mod.browser import Browser

class Testss(Browser):
    def __init__(self, ses) -> None:
        self.load_driver(ses)
        self.open_url("https://duckduckgo.com/?t=ffab&q=asyncio+Tasks&ia=web")

def test():
    ses = BrowserSession(name='test')
    t = Testss(ses)