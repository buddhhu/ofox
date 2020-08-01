import setuptools

setuptools.setup(
    name="orangefoxapi",
    version="1.0.0",
    author="MrYacha",
    author_email="yacha@orangefox.tech",
    description="Asynchronous OrangeFox Recovery API library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'aiohttp>=3.5.4,<4.0.0',
    ]
)
