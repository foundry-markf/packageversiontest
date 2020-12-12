from distutils.core import setup
import os
import subprocess


class NotAGitRepo(Exception):
    pass


class Git(object):
    def __init__(self):
        if not os.path.isdir(".git"):
            raise NotAGitRepo()

    def _exec(self, *args):
        cmds = ["git"] + list(args)
        output = subprocess.check_output(cmds)
        return output

    def latest_tag(self):
        try:
            return self._exec("describe", "--abbrev=0").decode('utf8').strip()
        except subprocess.CalledProcessError:
            return None

    def branch_name(self):
        return self._exec("rev-parse", "--abbrev-ref", "HEAD").decode('utf8').strip()

    def commit_count_since(self, ref):
        if ref:
            return int(self._exec("rev-list", "--count", "HEAD", f"^{ref}").decode('utf8').strip())
        else:
            return int(self._exec("rev-list", "--count", "HEAD").decode('utf8').strip())


def _get_version_from_scm():
    try:
        git = Git()
        tag = git.latest_tag()
        if tag:
            version = tag
            commit_count = git.commit_count_since(tag)
        else:
            # no tags exist on the repo, so it's never been released
            version = "0.0.0"
            commit_count = git.commit_count_since(None)

        if commit_count > 0:
            # progress has been made since the last release
            branch_name = git.branch_name()
            if branch_name == "master" or branch_name.startswith("v"):
                # master or maintenance branch
                version += f".dev{commit_count}"
            else:
                # feature branch; all commits have the same package version
                version += f"+{branch_name}"

        with open("version.py", "wt") as f:
            f.write(f"__version__='{version}'")
        return version
    except NotAGitRepo:
        version = {}
        with open("version.py") as f:
            exec(f.read(), version)
        return version["__version__"]


setup(
    name='packageversiontest',
    version=_get_version_from_scm(),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    py_modules=['packageversiontest'],
)
