# -*- coding: utf-8 -*-

import importlib

import pytest
from pony import orm


def _pg_reset_sequences(db):
    # with orm.db_session():
    sequences = db.execute(
        "SELECT sequence_name FROM information_schema.sequences;"
    ).fetchall()
    for item in sequences:
        req = "ALTER sequence {0} RESTART".format(item[0])
        db.execute(req)


def pytest_addoption(parser):
    """
    add option to inifile : where find db
    ex : bla.models if db in ./bla/models.py
    """

    parser.addini("PONY_DB", "pony db location")


def pytest_configure(config):
    """
    setup database and marker before session
    """

    # add marker to apply db_session to test
    config.addinivalue_line(
        "markers", "pony: mark a test with use of db_session and reset db "
    )

    # import test_database and reset it then create a fresh new database.
    db_path = config.getini("PONY_DB")
    db = importlib.import_module(db_path).db

    # and reset it then create a fresh new database.
    db.drop_all_tables(with_all_data=True)
    db.create_tables()


def pytest_runtest_setup(item):
    """
    Before each marked test, db_session is enabled
    """
    marker = item.get_closest_marker("pony")
    if marker and marker.kwargs.get("db_session", True):
        orm.db_session.__enter__()


def pytest_runtest_call(item):
    """
    The test starts by committing the uncommitted fixture. Resolve None PK if uncommitted
    """
    marker = item.get_closest_marker("pony")
    if marker:
        if marker.kwargs.get("db_session", True):
            orm.flush()
        else:
            with orm.db_session:
                orm.flush()


def _ponydb(item):
    """return db : test Database instance"""
    db_path = item.config.getini("PONY_DB")
    db = importlib.import_module(db_path).db
    return db


def pytest_runtest_teardown(item, nextitem):
    """

    """
    marker = item.get_closest_marker("pony")

    # import test db
    db = _ponydb(item)
    provider = db.provider.dialect

    if marker:
        if not marker.kwargs.get("db_session", True):
            orm.db_session.__enter__()
        # delete all entries from db at end of test
        # unless @pytest.mark.pony(reset_db=False) is specified

        if not marker.kwargs.get("db_session", True):
            orm.db_session.__enter__()

        if marker.kwargs.get("reset_db", True):
            orm.rollback()  # clear possible uncommitted things before delete so the base is Ok. Not good with
            # commit
            for entity in db.entities.values():
                orm.delete(e for e in entity)

            # reset sequence : postgres support
            if provider == "PostgreSQL":
                _pg_reset_sequences(db)
        # delete or not the db_session is closed
        orm.db_session.__exit__()


@pytest.fixture(scope="session")
def ponydb(request):
    """return db : test Database instance"""
    db_path = request.config.getini("PONY_DB")
    db = importlib.import_module(db_path).db
    return db
