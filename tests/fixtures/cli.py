import pytest
import traceback


import click


@pytest.fixture(scope='session')
def assert_output():
    def assert_output(result, msg, exit_code=0, **style):
        if result.exception:
            traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)
        assert result.exit_code == exit_code
        if style:
            assert bytes(click.style(str(msg), **style), 'UTF-8') in result.stdout_bytes
        else:
            assert str(msg) in result.output

    return assert_output
