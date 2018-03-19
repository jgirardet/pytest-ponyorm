from pony import orm

db = orm.Database()


class Bla(db.Entity):
    name = orm.Required(str)


db.bind(provider='sqlite', filename=':memory:')
db.generate_mapping(create_tables=True)
