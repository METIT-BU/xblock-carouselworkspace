import os
from setuptools import setup


def package_data(pkg, root_list):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for root in root_list:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='xblock-multimedia-workspace',
    version='0.1',
    description='XBlock - Multimedia-Workspace',
    packages=['workspace'],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': 'workspace = workspace:WorkspaceBlock',
    },
    package_data=package_data("workspace", ["templates", "public"]),
)
