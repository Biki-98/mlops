print(">>> USING THIS SETUP.PY FILE <<<")

import setuptools
from typing import List

with open("README.md","r", encoding="utf-8") as f:
    description = f.read()

# We don't want "-e ." in setup.py file.
HYPHEN_E_DOT = "-e ."

def get_requirements(file_path:str) -> List[str]:
    """
    This function will return the list of requirements
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]
    
    if HYPHEN_E_DOT in requirements:
        requirements.remove(HYPHEN_E_DOT)

    return requirements

__version__ = "0.0.0"

# REPO_NAME = "sample-mlops-project"
AUTHOR_USER_NAME = "Biki-98"
SRC_REPO = "mlops"
AUTHOR_EMAIL = "parthaskill98@gmail.com"

setuptools.setup(
    # name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package for a sample MLOPs project",
    long_description=description,
    long_description_content = "text/markdown",
    # url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=get_requirements("requirements.txt")

)

