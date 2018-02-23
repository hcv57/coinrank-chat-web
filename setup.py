from setuptools import setup

setup(
    name='coinrankchat-web',
    packages=['coinrankchat.web'],
    include_package_data=True,
    install_requires=[
        'flask', 'requests'
    ]
)
