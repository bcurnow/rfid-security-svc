import pytest
from unittest.mock import patch

from click.exceptions import MissingParameter

from rfidsecuritysvc.cli.test import generate_api_key

@patch('rfidsecuritysvc.cli.test.generate_password_hash')
def test_generate_test_apikey_value(generate_password_hash, runner):
    generate_password_hash.return_value = 'test'
    result = runner.invoke(args=['test', 'generate-test-apikey', 'test'])
    assert result.output == 'test\n'
    generate_password_hash.assert_called_once_with('test')

def test_generate_test_apikey_value_required():
    with pytest.raises(MissingParameter):
        generate_api_key.make_context('generate-api-key',[])

