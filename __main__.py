from scrapfishin.database import Database
from scrapfishin import models

from secrets import USER, HOST


if __name__ == '__main__':
    db = Database(f'postgresql://{USER}@{HOST}/snapfishin')
    print(db)

    models.Base.metadata.create_all(db.engine)
    print(models.Base.metadata.tables)
