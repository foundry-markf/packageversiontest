from distutils.core import setup


def _my_func(dist, attr, value):
    print("*****", dist, attr, value)
    dist.metadata.version = f"1.2.3+{value}"


setup(
    name='packageversiontest',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    entry_points={
        "distutils.setup_keywords": [
            "foo = setup:_my_func",
        ],
    },
    foo="Banana",
)
print("***** Finished!")
