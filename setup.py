from setuptools import find_packages,setup
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_PATH = os.path.join(BASE_DIR,"requirements.txt")

HYPEN_E_DOT = '-e .'

def get_requirements(file_path):
    requirements = []
    with open(file_path) as file_object:
        requirements = file_object.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements


setup(
    name="puzzle_world",
    version="1.0.0",
    author="ravibalebilalu",
    author_email="81ravikiran@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(REQUIREMENTS_PATH)
)