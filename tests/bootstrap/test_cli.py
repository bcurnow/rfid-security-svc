def test_bootstrap_registers_cli_group(app):
    """This test will simply ensure that all the expected top-level groups are available, test code for each cli module will do the rest"""
    with app.app_context():
        expected = ['auth', 'config', 'db', 'media', 'media-perm', 'permission', 'test']
        for cmd in app.cli.list_commands(app.app_context()):
            assert cmd in expected
