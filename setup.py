# setup.py

from setuptools import setup, find_packages

setup(
    name='github_grass_art',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'numpy',
    ],
    author='Joon Park',
    author_email='biasdrive@gmail.com',
    description='Create custom GitHub contribution graphs with art.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kafkapple/github_grass_art',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'github-grass-art=github_grass_art.main:main',
        ],
    },
)