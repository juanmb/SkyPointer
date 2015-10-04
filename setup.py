#!/usr/bin/env python

from setuptools import setup


setup(
    name='sky-pointer',
    version='0.1',
    url='https://github.com/juanmb/SkyPointer',
    license='MIT',
    author='Juan Menendez',
    install_requires=['pyserial', 'numpy'],
    author_email='juanmb@gmail.com',
    description='Software for controlling a motorized sky-pointing laser',
    packages=['sky_pointer'],
    platforms='any',
    entry_points={'console_scripts': ['sky-pointer = sky_pointer.main:main']},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
