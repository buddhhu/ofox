import setuptools

from orangefoxapi.version import version

setuptools.setup(
    name="orangefoxapi",
    version=version,
    author="Yacha",
    author_email="yacha@orangefox.tech",
    description="OrangeFox Recovery API library",
    packages=setuptools.find_packages(include=['orangefoxapi', 'orangefoxapi.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.25.0',
        'pydantic'
    ],
    extras_require={
        'async': ['aiohttp>=3.5.4,<4.0.0']
    }
)
