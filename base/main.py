import os
from dotenv import load_dotenv
from youtube import SessionManager, YoutubeBrowser

load_dotenv()

def test():
    YOUTUBE_LOGIN = os.getenv('YOUTUBE_LOGIN')
    YOUTUBE_PASSWORD = os.getenv('YOUTUBE_PASSWORD')
    YOUTUBE_CHANEL_NAME = os.getenv('YOUTUBE_CHANEL_NAME')
    ses = SessionManager().get_test_session()
    yt = YoutubeBrowser(ses=ses, login=YOUTUBE_LOGIN, password=YOUTUBE_PASSWORD, chanel_name=YOUTUBE_CHANEL_NAME)
    ...

if __name__ == "__main__":
    test()