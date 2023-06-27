from youtube import YoutubeBrowser, SessionManager

if __name__ == "__main__":
    ses = SessionManager().get_test_session()
    yb = YoutubeBrowser(ses, login="murmurshikcl1", password="s9gtLNvQ0FtOqzErjnk2L41zLunkbf5spYR", chanel_name="oleg")
    