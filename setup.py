from setuptools import setup
from pathlib import Path

with open(Path('./requirements.txt').resolve()) as f:
    required = f.read().splitlines()

setup(
    name="open_pose",  
    packages=["py", "py/utils", "py/pose_estimation"],
    install_requires=required,
    version="0.1.1"
)

