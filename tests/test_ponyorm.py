# -*- coding: utf-8 -*-
import pytest


def test_ponydb_(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        import tests.app

        def test_ponydb(ponydb):
            assert ponydb.entities['Bla']
    """
    )
    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_ponydb PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_db_ini_setting(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        import tests.app

        # @pytest.fixture
        # def ponydb(request):
        #     return request.config.getini('HELLO')

        def test_ponydb(ponydb):
            assert ponydb is tests.app.db
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_ponydb PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_marker_exist(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest

        pytestmark = pytest.mark.pony

        def test_marker_exist(request):
            marker = request.node.get_closest_marker('pony', None)
            assert marker.name == "pony"
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_marker_exist PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_marker_apply_db_session(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm

        pytestmark = pytest.mark.pony

        def test_marker_apply_db_session():
            a = db.Bla(name="omkmok")
            a.flush()
            assert a.id is not None
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_marker_apply_db_session PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_marker_do_not_apply_db_session_if_db_session_false(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm

        pytestmark = pytest.mark.pony(db_session=False)

        def test_marker_do_not_apply_db_session_if_db_session_false():
            with orm.db_session:
                a = db.Bla(name="omkmok")
                a.flush()
                assert a.id is not None
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_marker_do_not_apply_db_session_if_db_session_false PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_marker_drop_table(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
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

    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_1 PASSED*", "*::test_2 PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_marker_drop_table_with_db_session_false(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm

        pytestmark = pytest.mark.pony(db_session=False)

        def test_1():
            with orm.db_session:
                a = db.Bla(name="omkmok")
                a = db.Bla(name="omkmok")
                a = db.Bla(name="omkmok")
                orm.commit()
                assert db.Bla.select().count() == 3

        def test_2():
            with orm.db_session:
                a = db.Bla(name="omkmok")
                assert db.Bla.select().count() == 1

    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_1 PASSED*", "*::test_2 PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_marker_dont_drop_table(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm

        pytestmark = pytest.mark.pony

        @pytest.mark.pony(reset_db=False)
        def test_1():
            a = db.Bla(name="omkmok")
            a = db.Bla(name="omkmok")
            a = db.Bla(name="omkmok")
            assert db.Bla.select().count() == 3

        def test_2(request):
            a = db.Bla(name="omkmok")
            assert db.Bla.select().count() == 4
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_1 PASSED*", "*::test_2 PASSED*"])

    # # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_pony_marker_dont_drop_table_with_db_session_false(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm

        pytestmark = pytest.mark.pony(db_session=False)

        @pytest.mark.pony(reset_db=False, db_session=False)
        def test_1():
            with orm.db_session:
                a = db.Bla(name="omkmok")
                a = db.Bla(name="omkmok")
                a = db.Bla(name="omkmok")
                assert db.Bla.select().count() == 3

        def test_2(request):
            with orm.db_session:
                a = db.Bla(name="omkmok")
                assert db.Bla.select().count() == 4
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_1 PASSED*", "*::test_2 PASSED*"])

    # # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_plugin_commit_fixture_before_test(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
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
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_1 PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_plugin_commit_fixture_before_test_with_db_session_false(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm

        @pytest.fixture(scope='function')
        @orm.db_session
        def fixt(request):
            a = db.Bla(name="hello")
            # a.flush()
            return a

        @pytest.mark.pony(db_session=False)
        def test_1(fixt):
            with orm.db_session:
                assert fixt.id == 1
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_1 PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

def test_remove_relation_not_saved(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm

        @pytest.fixture(scope='function')
        def bla(request):
            return db.Bla(name="something")

        @pytest.mark.pony
        def test_1(bla):
            b = db.Ble(bla=bla, name="aha")
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_1 PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

@pytest.mark.skip
def test_remove_relation_not_saved_with_db_session_false(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm

        @pytest.fixture(scope='function')
        @orm.db_session
        def bla(request):
            return orm.make_proxy(db.Bla(name="something"))

        @pytest.mark.pony(db_session=False)
        def test_1(bla):
            with orm.db_session:
                b = db.Ble(bla=bla, name="aha")
                b.bla.update()
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_1 PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_reset_sequence_pgsql(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm

        pytestmark = pytest.mark.pony


        def test_1():
            a = db.Bla(name="omkmok")
            a.flush()
            assert a.id == 1

        def test_2(ponydb):
            # print(ponydb.execute("select * from sqlite_sequence").fetchall())
            a = db.Bla(name="omkmok")
            a.flush()
            # print(ponydb.execute("select * from sqlite_sequence").fetchall())

            assert a.id == 1
            # assert False
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_1 PASSED*", "*::test_2 PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


@pytest.mark.skip
def test_reset_sequence_pgsql_with_db_session_false(testdir):
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm

        pytestmark = pytest.mark.pony(db_session=False)


        def test_1():
            with orm.db_session:
                a = db.Bla(name="omkmok")
                a.flush()
                assert a.id == 1

        def test_2(ponydb):
            with orm.db_session:
                # print(ponydb.execute("select * from sqlite_sequence").fetchall())
                a = db.Bla(name="omkmok")
                a.flush()
                # print(ponydb.execute("select * from sqlite_sequence").fetchall())
    
                assert len(list(db.Bla.select())) == 1
                # assert False
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_1 PASSED*", "*::test_2 PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_delete_fixture_error_with_reverse(testdir):
    """
    If a fixture is created using a factory for the
    relatioship it should not fail
    """
    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm

        pytestmark = pytest.mark.pony

        def blafactory():
            return db.Bla(name="nomdebla")

        @pytest.fixture(scope='function')
        def ble():
            return db.Ble(name="nomdeble", bla=blafactory())


        def test_1(ble):
            ble.delete()
            assert ble.id

        # def test_2(ponydb):
        #     # print(ponydb.execute("select * from sqlite_sequence").fetchall())
        #     a = db.Bla(name="omkmok")
        #     a.flush()
        #     # print(ponydb.execute("select * from sqlite_sequence").fetchall())

        #     assert a.id == 1
        #     # assert False
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_1 PASSED*",
            # '*::test_2 PASSED*',
        ]
    )

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


@pytest.mark.skip
def test_delete_fixture_error_with_reverse_with_db_session_false(testdir):
    """
    If a fixture is created using a factory for the
    relatioship it should not fail
    """
        testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm
        pytestmark = pytest.mark.pony(db_session=False)

        def blafactory():
            return db.Bla(name="nomdebla")

        @pytest.fixture(scope='function')
        @orm.db_session
        def ble():
            return orm.make_proxy(db.Ble(name="nomdeble", bla=blafactory()))


        def test_1(ble):
            with orm.db_session:
                ble.delete()
                assert ble.id
      """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_1 PASSED*",
            # '*::test_2 PASSED*',
        ]
    )

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

def test_db_session_not_active_with_db_session_equal_false(testdir):

    testdir.makeini(
        """
        [pytest]
        PONY_DB=tests.app
    """
    )

    testdir.makepyfile(
        """
        import pytest
        from tests.app import db
        from pony import orm
        pytestmark = pytest.mark.pony

        @pytest.mark.pony(db_session=False)
        def test_1():
            with pytest.raises(orm.TransactionError):
                a = db.Bla(name="omkmok")
        

        def test_2(request):
            a = db.Bla(name="omkmok")
            assert a.name == "omkmok"
      """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally

    result.stdout.fnmatch_lines(
        [
            "*::test_1 PASSED*",
            # '*::test_2 PASSED*',
        ]
    )

    # make sure that that we get a '0' exit code for the testsuite

    result.stdout.fnmatch_lines(["*::test_1 PASSED*", "*::test_2 PASSED*"])

    # # make sure that that we get a '0' exit code for the testsuite

    assert result.ret == 0
