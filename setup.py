from setuptools import setup, find_packages

setup(
    name="DJSetFiller",
    packages=find_packages(where='src'),
    include_package_data=True,
    package_dir={'': 'src'},
)
