# packageversiontest

Prototype for determining a package version from git using PEP440 guidelines.
This differs from other solutions available publicly in the way it handles feature branch names.

setup.py generates a version.py (git ignored) with a __version__ attribute that is read by the module itself.
This also solves what to do with source distributions (python setup.py sdist) as the version.py is encoded into that, and the setup.py functions query whether a git repo is present or not, and reads version.py directory if not.
