# -*- coding: utf-8 -*-

import pytest
import importlib
from pony import orm


def pytest_addoption(parser):
    parser.addini('PONY_DB', 'pony db location')


@pytest.fixture(scope='session', autouse=True)
def ponydb(request):
    """return db : main Database instance"""
    db_path = request.config.getini('PONY_DB')
    db = importlib.import_module(db_path).db
    return db


@pytest.fixture(scope='function')
def _db_session(request):
    """ Use db_session context manager inside tests """
    with orm.db_session:
        yield


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "pony: mark a test with use of db_sesion and reset db ")


@pytest.fixture(autouse=True)
def marker(request):
    """ marker for ponyorm """
    marker = request.keywords.get('pony', None)
    if marker:
        request.getfixturevalue('_db_session')


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
            print('dop_create')
            db.create_tables()
