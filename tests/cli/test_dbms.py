from unittest.mock import patch


@patch('rfidsecuritysvc.cli.dbms.dbms')
def test_init_db(dbms, runner, assert_output):
    dbms.init_db.return_value = None
    result = runner.invoke(args=['db', 'init'], input='y')
    assert_output(result, 'Are you sure, this will delete all current data?')
    assert_output(result, 'Initialized the database.')


@patch('rfidsecuritysvc.cli.dbms.dbms')
def test_init_db_no(dbms, runner, assert_output):
    result = runner.invoke(args=['db', 'init'], input='n')
    assert_output(result, 'Are you sure, this will delete all current data?', 1)
    dbms.init_db.assert_not_called()
