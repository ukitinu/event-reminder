try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name="event-reminder",
    version="1.0.0",
    description="Show messages at a specific date with crontab-like scheduling expressions.",
    author="ukitinu",
    author_email="ukitinu@gmail.com",
    url="https://github.com/ukitinu/event-reminder",
    packages=['eventreminder', 'eventreminder.tests'],
    license="MIT",
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='crontab birthday',
    include_package_data=True,
)
