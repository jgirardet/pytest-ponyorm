from pony import orm

db = orm.Database()


class Bla(db.Entity):
    name = orm.Required(str)
    champs = orm.Optional(str)
    bles = orm.Set('Ble')


# db_params = dict(
#     provider="postgres",
#     host="localhost",
#     database="mapistar3",
#     user="j",
#     password="j",
#     port=5432,
#     # create_tables=True,
# )


class Ble(db.Entity):
    name = orm.Required(str)
    bla = orm.Required(Bla)


db.bind(provider='sqlite', filename=':memory:')
db.generate_mapping(create_tables=True)
