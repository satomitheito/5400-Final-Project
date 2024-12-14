import setuptools
with open('README.md', 'r') as f:
    long_description = f.read()
setuptools.setup(
name='JANAS',
version='0.0.1',
author='Satomi Ito & Samyu Vakkalanka & Trey Roark',
author_email='si408@georgetown.edu & spv15@georgetown.edu & rgr45@georgetown.edu',
description='Sentiment Analysis', long_description=long_description, long_description_content_type='text/markdown', packages=setuptools.find_packages(), python_requires='>=3.6',
extras_requres={"dev": ["pytest", "flake8", "autopep8"]}
)