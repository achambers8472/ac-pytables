import setuptools

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='simtables',
    version='0.0.1',
    author='Alexander Chambers',
    author_email='alexander.chambers8472@gmail.com',
    description='Simple tables',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/achambers8472/ac-pytables',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
