from setuptools import setup
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

# Read the version number from a source file.
# Why read it, and not import?
# see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(name='slackeventsapi',
      version=find_version('slackeventsapi', 'version.py'),
      description='Python Slack Events API adapter',
      url='http://github.com/slackapi/python-slack-events-api',
      author='Slack',
      author_email='opensource@slack.com',
      license='MIT',
      packages=['slackeventsapi'],
      install_requires=[
        'flask',
        'pyee',
        'requests',
        'six',
      ],
      zip_safe=False)
