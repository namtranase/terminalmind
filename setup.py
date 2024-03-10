from setuptools import setup, find_packages

setup(
    name='temi',
    version='2.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'temi = src.temi_interface:main',
        ],
    },
    # Add all necessary package requirements here
    install_requires=[
        'requests',
        # Add other dependencies needed for your package
    ],
    # Metadata
    author='Nam Tran',
    author_email='trannam.ase@gmail.com',
    description='An assistant in your terminal powered by llama.cpp',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/namtranase/terminalmind',  # Use the URL to the github repo.
    project_urls={
        'Source': 'https://github.com/namtranase/terminalmind',
        # Add any other relevant links here
    },
)
