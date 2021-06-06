from pytest_timestamper import _version


def test_has_version():
    _version.version_tuple is not None
