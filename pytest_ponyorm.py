# -*- coding: utf-8 -*-

import pytest
import importlib
from pony import orm


def pytest_addoption(parser):
    parser.addini('PONY_DB', 'pony db location')


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "pony: mark a test with use of db_sesion and reset db ")

    db_path = config.getini('PONY_DB')
    db = importlib.import_module(db_path).db
    db.drop_all_tables(with_all_data=True)
    db.create_tables()


@pytest.fixture(scope='session', autouse=True)
def ponydb(request):
    """return db : main Database instance"""
    db_path = request.config.getini('PONY_DB')
    db = importlib.import_module(db_path).db
    return db


# @pytest.fixture(scope='function')
# def _db_session(request):
#     """ Use db_session context manager inside tests """
#     with orm.db_session:
#         yield

# @pytest.fixture(autouse=True)
# def marker(request):
#     """ marker for ponyorm """
#     marker = request.keywords.get('pony', None)
#     if marker:
#         request.getfixturevalue('_db_session')


def pytest_runtest_setup(item):
    """
    Before each test, database is cleared unless "reset_db" is False :
    @pytest.mark.pony(reset_db=False)
    """
    marker = item.get_marker('pony')
    if marker:
        if marker.kwargs.get('reset_db', True):
            # rest db before running test
            db = ponydb(item)
            db.drop_all_tables(with_all_data=True)
            db.create_tables()


def pytest_runtest_setup(item):
    """
    Before each test, database is cleared unless "reset_db" is False :
    @pytest.mark.pony(reset_db=False)
    """
    marker = item.get_marker('pony')
    if marker:
        orm.db_session.__enter__()


# def pytest_fixture_setup(fixturedef, request):
#     marker = request.keywords.get('pony', None)


def pytest_runtest_call(item):
    marker = item.get_marker('pony')
    if marker:
        orm.commit()


def pytest_runtest_teardown(item, nextitem):
    marker = item.get_marker('pony')
    db_path = item.config.getini('PONY_DB')
    db = importlib.import_module(db_path).db

    if marker:
        orm.commit()
        for entity in db.entities.values():
            entity.select().delete(bulk=True)
        orm.db_session.__exit__()