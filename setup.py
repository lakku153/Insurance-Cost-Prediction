from setuptools import find_packages, setup


def get_requirements(file_path):
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        [req.replace('\n','') for req in requirements]

        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements

setup(
    name='Insurance project',
    version='0.0.1',
    author='lokesh',
    author_email='lokesh726888@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)