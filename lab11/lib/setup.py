from setuptools import setup, find_packages

setup(
    name='python-example-lib',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='An example python package',
    long_description=open('README.md').read(),
    url='https://github.com/KacperBieganek/good-programing-practises/tree/master/lab11/lib',
    author='Kacper Bieganek',
    author_email='KacBieganek@gmail.com'
)