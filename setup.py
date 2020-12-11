from distutils.core import setup
import subprocess


class Git(object):
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
            return int(self._exec("rev-list", "--count", "HEAD", f"^{{{ref}}}").decode('utf8').strip())
        else:
            return int(self._exec("rev-list", "--count", "HEAD").decode('utf8').strip())


def _get_version_from_scm(dist, attr, value):
    if not value:
        return

    git = Git()
    tag = git.latest_tag()
    if tag:
        version = tag
    else:
        # no tags exist on the repo, so it's never been released
        version = "0.0.0"

    branch_name = git.branch_name()
    if branch_name == "master" or branch_name.startswith("v"):
        # master or maintenance branch
        if tag:
            commit_count = git.commit_count_since(tag)
        else:
            commit_count = git.commit_count_since(None)
        if commit_count > 0:
            # progress has been made since the last release
            version += f".dev{commit_count}"
    else:
        # feature branch; all commits have the same package version
        version += f"+{branch_name}"

    dist.metadata.version = version


setup(
    name='packageversiontest',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    entry_points={
        "distutils.setup_keywords": [
            "version_from_scm = setup:_get_version_from_scm",
        ],
    },
    version_from_scm=True,
)
