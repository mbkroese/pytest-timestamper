import setuptools

setuptools.setup(
    name="pytest-timestamper",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"pytest11": ["name_of_plugin = pytest_timestamper.plugin"]},
    classifiers=["Framework :: Pytest"],
    use_scm_version={"write_to": "src/pytest_timestamper/_version.py"},
    setup_requires=["setuptools-scm"],
)
