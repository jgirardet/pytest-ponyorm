import os
from urllib.parse import urlparse

from pony import orm

db = orm.Database()


class Bla(db.Entity):
    name = orm.Required(str)
    champs = orm.Optional(str)
    bles = orm.Set('Ble')

    def update(self):
        self.champs = "LALA"

 
class Ble(db.Entity):
    name = orm.Required(str)
    bla = orm.Required(Bla)

    # def after_insert(self):
    #     self.bla.update()

    def before_delete(self):
        self.bla.update()




def bind_db(db):
    bdb = os.environ['DB_PROVIDER']
    if bdb == "sqlite":
        db.bind(provider='sqlite', filename=':memory:')
    elif bdb == "postgres":
        url = urlparse(os.environ['PG_PONY_DB'])
        db.bind(
            provider=url.scheme,
            host=url.hostname,
            database=url.path.strip('/'),
            user=url.username,
            password=url.password,
            port=url.port,
            # create_tables=True,
            )

bind_db(db)

db.generate_mapping(create_tables=True)
