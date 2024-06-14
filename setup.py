from setuptools import setup, find_packages

setup(
    name="srt-web-chat",
    version="0.1.0",
    author="SolidRusT Networks",
    author_email="info@solidrust.net",
    description="A modular web chat application integrating srt-core and llama-cpp-agent frameworks.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SolidRusT/srt-web-chat",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=[
        "srt-core",
        "llama-cpp-agent",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

