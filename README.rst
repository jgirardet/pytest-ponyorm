==============
pytest-ponyorm
==============

.. image:: https://img.shields.io/pypi/v/pytest-ponyorm.svg
    :target: https://pypi.python.org/pypi/pytest-ponyorm
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-ponyorm.svg
    :target: https://pypi.python.org/pypi/pytest-ponyorm
    :alt: Python versions

.. image:: https://travis-ci.org/jgirardet/pytest-ponyorm.svg?branch=master
    :target: https://travis-ci.org/jgirardet/pytest-ponyorm
    :alt: See Build Status on Travis CI

PonyORM in Pytest

----

Plugin for use `Pony ORM`_ in `Pytest`_.

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.


Features
--------

* Access Database instance (db) via *ponydb* fixture
* Mark tests to auto allow use of *pony.orm.db_session*
* Database is by default cleared after each test
* Database reset can be cancelled for test/class/module


Requirements
------------

Tested from `Pony ORM`_ >= '0.7.3' and python : 3.5, 3.6


Installation
------------

You can install "pytest-ponyorm" via `pip`_ from `PyPI`_::

    $ pip install pytest-ponyorm
    or
    $ pipenv install -d pytest-ponyorm


Usage
-----

.. warning:: By default, database is cleared after each test. You must never use it in a production environment. This plugin doesn't change the database config.It's you'job to create the testing environment and change database params.

First, configure PONY_DB in pytest.ini. PonyORM main Database instance  module location must be specified in pytest.ini to make it work : for example if db is in /path/models/main.py, you must configure like this :

.. code-block:: ini

    [pytest]
	PONY_DB=path.models.main

Then just apply the pony marker :

.. code-block:: python

    # models.py

    db = Database()

    # test.py

    @pytest.mark.pony
    def my_test(ponydb):
        new_mod = ponydb.Mymodel(name="me",...)

You can mark a class or function with @pytest.mark.pony or the whole module with pytestmark = pytest.mark.pony

The marker *pony* takes one argument : *reset_db*, default is True. In this case the marked test doesn't reset the database at ending.

.. code-block:: python
	
	# test.py
    pytestmark = pytest.mark.pony # marks all tests of the module

    def test1:
    	pass

    def test2:
    	pass

    @pytest.mark.pony(reset_db=False)
    def test 3:
    	pass

    # test3 will use database in the state that test2 left it.

About Reseting Database:
-------------------------
Test database tables are dropped/recreate before the test SESSION.

Initialy this plugin did drop/recreate table  for each test. Due to perfomance reason, this has changed. Now tables are cleared but not dropped. 


Sql sequences like  "auto PrimaryKey"  will also be reset but actually, it's only supported for PostgreSQL and Sqlite. For other databases, Primarykey might not start at 1 for each test. This has to be considered when writing tests.



About Fixtures :
-----------------
Fixtures should not use db_session decorator or context manager. Each test is automaticaly run inside a db_session  and each operation inside fixtures will be commited at test start.


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.


License
-------

Distributed under the terms of the `GNU GPL v3.0`_ license, "pytest-ponyorm" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.


Changelog
----------
0.3.1 :
    - sql sequence reset for postgre and sqlite
    - testing py35/36 and pg/sqlite
0.3.0 :     
    - made faster with just deleting database entries after each test
    - no drop/recreate
    - db_session splitted into 2 hooks, not anymore in a fixture
0.2.9 :
    - add fixture autocommit before run test
0.2.0 :
    - add marker
0.1.5 :
    - add db_session for each test
0.1.0 :
    - auto clear database


.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/jgirardet/pytest-ponyorm/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`Pony ORM`: http://ponyorm.com
.. _`pytest-env`: https://github.com/MobileDynasty/pytest-env
