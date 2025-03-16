from setuptools import setup, find_packages

setup(
    name="jutix",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "tqdm>=4.65.0",
        "dynaconf>=3.2.0",
        "loguru>=0.7.0",
    ],
    entry_points={
        'console_scripts': [
            'jutix=jutix.main:main',
        ],
    },
    author="Sachin Duhan",
    author_email="duhan.sachin126@gmail.com",  # Add your email if desired
    description="A JMeter JTL output analysis tool",
    long_description=open("README.md").read() if open("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/sachin-duhan/jutix",  # Add your repository URL if desired
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 