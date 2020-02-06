from selenium import webdriver

from scrapfishin import vendor_dir


class Chrome(webdriver.Chrome):

    def __init__(self, *options):
        opts = webdriver.ChromeOptions()
        [opts.add_argument(option) for option in options]
        super().__init__(str(vendor_dir / 'chromedriver.exe'), options=opts)
