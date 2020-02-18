import pathlib

from selenium import webdriver


class Chrome(webdriver.Chrome):

    def __init__(self, *options):
        opts = webdriver.ChromeOptions()
        [opts.add_argument(option) for option in options]
        exe = pathlib.Path(__file__).parent / 'vendor' / 'chromedriver.exe'
        super().__init__(str(exe), options=opts)
