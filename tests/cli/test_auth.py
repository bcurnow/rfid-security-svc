from unittest.mock import patch


@patch('rfidsecuritysvc.cli.auth.auth')
def test_generate_api_key(auth, runner, assert_output):
    auth.generate_api_key.return_value = 'test'
    result = runner.invoke(args=['auth', 'generate-api-key'], input='y', color=True)
    assert_output(result, 'Are you sure, this will invalidate the old key?')
    assert_output(result, 'Generated new key "test", please record this value as it is not retrievable.', bg='green', fg='black')
    auth.generate_api_key.assert_called_once()


@patch('rfidsecuritysvc.cli.auth.auth')
def test_generate_api_key_with_confirm_option(auth, runner, assert_output):
    auth.generate_api_key.return_value = 'test'
    result = runner.invoke(args=['auth', 'generate-api-key', '--yes'], color=True)
    assert 'Are you sure, this will invalidate the old key?' not in result.output
    assert_output(result, 'Generated new key "test", please record this value as it is not retrievable.', bg='green', fg='black')
    auth.generate_api_key.assert_called_once()


@patch('rfidsecuritysvc.cli.auth.auth')
def test_generate_api_key_no(auth, runner, assert_output):
    result = runner.invoke(args=['auth', 'generate-api-key'], input='n', color=True)
    assert_output(result, 'Are you sure, this will invalidate the old key?', 1)
    auth.generate_api_key.assert_not_called()
