import setuptools

setuptools.setup(
    name="pytest-timestamper",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"pytest11": ["name_of_plugin = pytest_timestamper.plugin"]},
    use_scm_version={"write_to": "src/pytest_timestamper/_version.py"},
    classifiers=[
        "Framework :: Pytest",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
