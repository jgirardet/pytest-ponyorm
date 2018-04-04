import os

from pony import orm

db = orm.Database()

mode = os.environ['MYPROJECT_MODE']

if mode == "memory":
    DB_PARAMS = {
        "provider": "sqlite",
        "filename": ":memory:",
        # "create_db":True,
    }
elif mode == "sqlite":
    DB_PARAMS = {
        "provider": "sqlite",
        "filename": "/tmp/sqlite.db",
        "create_db": True,
    }
elif mode == "pgsql":
    DB_PARAMS = {
        'provider': 'postgres',
        'database': 'pytestponyorm',
        'host': 'localhost',
        'port': 5432,
        'user': 'j',
        'password': 'j'
    }


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


db.bind(**DB_PARAMS)

db.generate_mapping(create_tables=True)
