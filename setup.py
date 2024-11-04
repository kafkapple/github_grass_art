# setup.py

from setuptools import setup, find_packages

setup(
    name="github_grass_art",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pillow",
        "numpy",
        "scipy",
    ],
    entry_points={
        'console_scripts': [
            'github-grass-art=github_grass_art.main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Create art with GitHub contribution graph",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kafkapple/github_grass_art",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)