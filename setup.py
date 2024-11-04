# setup.py

from setuptools import setup, find_packages

setup(
    name='github_grass_art',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'numpy',
        # 필요 시 다른 라이브러리 추가
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='Create custom GitHub contribution graphs with art.',
    url='https://github.com/yourusername/github_grass_art',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)