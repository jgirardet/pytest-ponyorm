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

db = bind_db(db)

# db.generate_mapping(create_tables=True)
