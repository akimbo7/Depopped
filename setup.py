from distutils.core import setup

setup(
    name='Depopped',
    version='1.0.0',
    author='akimbo',
    author_email='akimbo7@protonmail.com',
    packages=['depopped',],
    url='https://github.com/akimbo7/Depopped',
    license='LICENSE',
    python_requires='>=3.7.0',
    description='A simple API Wrapper for Depop.',
    long_description=open('README.md').read(),
    install_requires=[
        "requests>=2.26.0",
        "uuid>=1.30",
        "colorama>=0.4.4"
    ],
)
