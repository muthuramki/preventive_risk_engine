from setuptools import setup, find_packages

setup(
    name="preventive-risk-engine",
    version="2.1.0",
    packages=find_packages(include=["preventive_risk_engine", "preventive_risk_engine.*"]),
    install_requires=["PyYAML>=6.0"],
    python_requires=">=3.9",
    include_package_data=True,
)
