from distutils.core import setup

setup(
    name='packageversiontest',
    long_description=open('README.md').read(),
    setup_requires=['setuptools-git-versioning'],
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}.dev{ccount}+git.{sha}",
        "dirty_template": "{tag}.dev{ccount}+git.{sha}.dirty",
        "starting_version": "0.0.0",
        "version_callback": None,
        "version_file": None,
        "count_commits_from_version_file": False
    },
)
