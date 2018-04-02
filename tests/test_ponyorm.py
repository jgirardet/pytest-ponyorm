# -*- coding: utf-8 -*-

# def tesst_bar_fixture(testdir):
#     """Make sure that pytest accepts our fixture."""

#     # create a temporary pytest test module
#     testdir.makepyfile("""
#         def tesst_sth(bar):
#             assert bar == "europython2015"
#     """)

#     # run pytest with the following cmd args
#     result = testdir.runpytest('--foo=europython2015', '-v')

#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines([
#         '*::tesst_sth PASSED*',
#     ])

#     # make sure that that we get a '0' exit code for the testsuite
#     assert result.ret == 0

# def tesst_help_message(testdir):
#     result = testdir.runpytest('--help', )
#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines([
#         'ponyorm:',
#         '*--foo=DEST_FOO*Set the value for the fixture "bar".',
#     ])


def test_ponydb_(testdir):
    testdir.makeini("""
        [pytest]
        PONY_DB=tests.app
    """)

    testdir.makepyfile("""
        import pytest
        import tests.app

        def test_ponydb(ponydb):
            assert ponydb
    """)
    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_ponydb PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_db_ini_setting(testdir):
    testdir.makeini("""
        [pytest]
        PONY_DB=tests.app
    """)

    testdir.makepyfile("""
        import pytest
        import tests.app

        # @pytest.fixture
        # def ponydb(request):
        #     return request.config.getini('HELLO')

        def test_ponydb(ponydb):
            assert ponydb is tests.app.db
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_ponydb PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_marker_exist(testdir):
    testdir.makeini("""
        [pytest]
        PONY_DB=tests.app
    """)

    testdir.makepyfile("""
        import pytest

        pytestmark = pytest.mark.pony

        def test_marker_exist(request):
            marker = request.keywords.get('pony', None)
            assert marker.name == "pony"
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_marker_exist PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_marker_apply_db_session(testdir):
    testdir.makeini("""
        [pytest]
        PONY_DB=tests.app
    """)

    testdir.makepyfile("""
        import pytest
        from tests.app import db
        from pony import orm

        pytestmark = pytest.mark.pony

        def test_marker_apply_db_session():
            a = db.Bla(name="omkmok")
            assert a.to_dict() == {'id':1, 'name':"omkmok"}
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_marker_apply_db_session PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_marker_drop_table(testdir):
    testdir.makeini("""
        [pytest]
        PONY_DB=tests.app
    """)

    testdir.makepyfile("""
        import pytest
        from tests.app import db
        from pony import orm

        pytestmark = pytest.mark.pony

        def test_1():
            a = db.Bla(name="omkmok")
            a = db.Bla(name="omkmok")
            a = db.Bla(name="omkmok")
            orm.commit()
            assert db.Bla.select().count() == 3

        def test_2():
            a = db.Bla(name="omkmok")
            assert db.Bla.select().count() == 1

    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_1 PASSED*',
        '*::test_2 PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


# def test_pony_marker_dont_drop_table(testdir):
#     testdir.makeini("""
#         [pytest]
#         PONY_DB=tests.app
#     """)

#     testdir.makepyfile("""
#         import pytest
#         from tests.app import db
#         from pony import orm

#         pytestmark = pytest.mark.pony

#         def test_1():
#             a = db.Bla(name="omkmok")
#             a = db.Bla(name="omkmok")
#             a = db.Bla(name="omkmok")
#             assert db.Bla.select().count() == 3

#         @pytest.mark.pont(reset_db=False)
#         def test_2():
#             a = db.Bla(name="omkmok")
#             assert db.Bla.select().count() == 1
#     """)

#     result = testdir.runpytest('-v')

#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines([
#         '*::test_1 PASSED*',
#         '*::test_2 PASSED*',
#     ])

#     # make sure that that we get a '0' exit code for the testsuite
#     assert result.ret == 0


def test_plugin_commit_fiture_before_test(testdir):
    testdir.makeini("""
        [pytest]
        PONY_DB=tests.app
    """)

    testdir.makepyfile("""
        import pytest
        from tests.app import db
        from pony import orm

        # @orm.db_session
        @pytest.fixture(scope='function')
        def fixt(request):
            a = db.Bla(name="hello")
            # a.flush()
            return a

        @pytest.mark.pony
        def test_1(fixt):
            assert fixt.id == 1
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_1 PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
