import pytest

import click


@pytest.fixture
def assert_output():
    def assert_output(result, msg, exit_code=0, **style):
        assert result.exit_code == exit_code
        if style:
            assert bytes(click.style(str(msg), **style), 'UTF-8') in result.stdout_bytes
        else:
            assert str(msg) in result.output

    return assert_output
