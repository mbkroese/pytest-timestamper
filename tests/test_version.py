from pytest_timestamper import _version


def test_has_version():
    major, minor, patch = _version.version_tuple
    assert major is not None
    assert minor is not None
    assert patch is not None
