from distutils.core import setup

setup(
    name='adusk',
    version='',
    packages=['adusk'],
    scripts=['bin/adusk'],
    data_files=[
        ('share/adusk/cfg/', ["data/cfg/keyboard-layout.yaml"])
    ],
    url='https://github.com/archshift/adusk',
    license='GPL3',
    author='archshift',
    author_email='',
    description='',
    requires=['pysdl2'],
)
