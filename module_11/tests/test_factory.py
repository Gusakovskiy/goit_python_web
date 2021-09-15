from module_11.personal_app import create_app


def test_app_factory_with_config():
    assert not create_app().testing  # assert default config is not testing
    assert not create_app().debug  # assert default config is not debug
    assert create_app({'TESTING': True}).testing
