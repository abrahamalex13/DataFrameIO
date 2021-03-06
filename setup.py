from pathlib import Path
import setuptools

DIR_ROOT = Path(__file__).resolve().parent
DIR_PACKAGE = DIR_ROOT / 'DataFrameIO'
DIR_REQS = DIR_ROOT / 'requirements'

with open(DIR_PACKAGE / "VERSION") as f:
    _version = f.read().strip()
    VERSION = _version

# setup requires Python list of required pkg
PATH_REQS = DIR_REQS / "requirements.txt"
def list_reqs(filename=PATH_REQS):
    with open(filename) as f:
        return f.read().splitlines()

setuptools.setup(
    name="DataFrameIO"
    , version=VERSION
    , author="Alex Abraham"
    , author_email="earlyassessments@gmail.com"
    , description="Interface for DataFrame reads & writes (especially via S3)"
    , install_requires=list_reqs()
    , packages=setuptools.find_packages(
        exclude=("tests")
        )
    , package_data={"DataFrameIO": ["VERSION"]}
    , include_package_data=True
    )