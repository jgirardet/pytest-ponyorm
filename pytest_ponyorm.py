# -*- coding: utf-8 -*-

import importlib

import pytest
from pony import orm


def _pg_reset_sequences(db):
    # with orm.db_session():
    sequences = db.execute(
        'SELECT sequence_name FROM information_schema.sequences;').fetchall()
    for item in sequences:
        req = 'ALTER sequence {0} RESTART'.format(item[0])
        db.execute(req)


def pytest_addoption(parser):
    """
    add option to inifile : where find db
    ex : bla.models if db in ./bla/models.py
    """

    parser.addini('PONY_DB', 'pony db location')


def pytest_configure(config):
    """
    setup database and marker before session
    """

    # add marker to apply db_sesssion to test
    config.addinivalue_line(
        "markers", "pony: mark a test with use of db_sesion and reset db ")

    # import test_database and reset it then create a fresh new database.
    db_path = config.getini('PONY_DB')
    db = importlib.import_module(db_path).db

    # and reset it then create a fresh new database.
    db.drop_all_tables(with_all_data=True)
    db.create_tables()


def pytest_runtest_setup(item):
    """
    Before each marked test, db_session is enabled
    """
    marker = item.get_marker('pony')
    if marker:
        orm.db_session.__enter__()


def pytest_runtest_call(item):
    """
    The test starts by committing the uncommited fixture. Resolve None PK if uncommited
    """
    marker = item.get_marker('pony')
    if marker:
        orm.flush()

def pytest_runtest_teardown(item, nextitem):
    """

    """
    marker = item.get_marker('pony')

    # import test db
    db = ponydb(item)
    provider = db.provider.dialect

    if marker:
        # delete all entries from db at end of test
        # unless @pytest.mark.pony(reset_db=False) is specified
        if marker.kwargs.get('reset_db', True):
            orm.rollback(
            )  # clear possible uncommited things before delete so the base is Ok. Not good with
            # commit
            for entity in db.entities.values():
                orm.delete(e for e in entity)

            # reset sequence : postres support
            if provider == 'PostgreSQL':
                _pg_reset_sequences(db)
        # delete or not the db_session is closed
        orm.db_session.__exit__()


@pytest.fixture(scope='session')
def ponydb(request):
    """return db : test Database instance"""
    db_path = request.config.getini('PONY_DB')
    db = importlib.import_module(db_path).db
    return db
