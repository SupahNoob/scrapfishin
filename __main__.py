from scrapfishin import Scrap

from secrets import USER, PASS, HOST


if __name__ == '__main__':
    scrap = Scrap(f'postgresql://{USER}:{PASS}@{HOST}/scrapfishin')
