from setuptools import setup

setup(
    name='terminalmind',
    version='0.0.1',    
    description='',
    url='https://github.com/namtranase/terminalmind',
    author='Nam Duc Tran',
    author_email='namngudan@gmail.com',    
    license='BSD 2-clause',
    packages=['terminalmind'],
    install_requires=['pytest',
                      'pylind',
                      'black',
                      'pre-commit'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)    