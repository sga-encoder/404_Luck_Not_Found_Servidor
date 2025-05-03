from setuptools import setup, find_packages

setup(
    name="casino-virtual",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Aquí puedes listar las dependencias del proyecto
    ],
    entry_points={
        "console_scripts": [
            "casino-virtual=src.main:main",  # Cambia 'main' y 'main' según tu función principal
        ],
    },
    author="sga-encoder",
    author_email="sebastian.garzon54795@ucaldas.edu.co",
    description="Descripción de tu proyecto",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sga-encoder/Casino-Virtual.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
