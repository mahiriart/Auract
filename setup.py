from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='Auract',
    version='0.9',
    description='Auract: tool to get right input for Microreact and auspice',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Iry63/Auract',
    author='Mateo Hiriart',
    license='GPLv3',
    packages=['auract'],
    package_data = {'auract': ['data/config/*','data/geodata/*']},
    install_requires=['pandas', 'nextstrain-augur', 'Jinja2'],
    entry_points={"console_scripts": [
            "auract = auract.__main__:main",
        ]},
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.8'
)