from setuptools import setup, find_packages

setup(
    name="image_collages",
    version="0.1.0",
    description="Genera collages con titulos y subtitulos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dobbie",
    author_email="tu_email@example.com",
    url="https://github.com/tu_usuario/tu_repositorio",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",       
        "matplotlib>=3.4.0",
        "pandas>=1.3.0",
        "Pillow>=8.2.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "black", "flake8"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "nombre_comando=nombre_del_paquete.modulo:funcion_principal",#Not sure about this part
        ],
    },
)
