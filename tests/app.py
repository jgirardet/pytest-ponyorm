from pony import orm

db = orm.Database()


class Bla(db.Entity):
    name = orm.Required(str)


# db_params = dict(
#     provider="postgres",
#     host="localhost",
#     database="mapistar3",
#     user="j",
#     password="j",
#     port=5432,
#     # create_tables=True,
# )

db.bind(provider='sqlite', filename=':memory:')
db.generate_mapping(create_tables=True)
