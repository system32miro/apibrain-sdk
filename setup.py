from setuptools import setup, find_packages
from pathlib import Path

# Ler README com encoding correto
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="apibrain-sdk",
    version="0.1.1",
    author="system32miro",
    author_email="seu.email@exemplo.com",
    description="SDK para criar APIs auto-descritivas compatíveis com agentes IA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/system32miro/apibrain-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "fastapi>=0.68.0",
        "pydantic>=1.8.0",
        "uvicorn>=0.15.0"
    ],
    project_urls={
        "Bug Reports": "https://github.com/system32miro/apibrain-sdk/issues",
        "Source": "https://github.com/system32miro/apibrain-sdk",
        "Documentation": "https://github.com/system32miro/apibrain-sdk#readme"
    }
) 