from setuptools import setup, find_packages

VERSION = "0.0.1"

install_requires = [
    # 必要な依存ライブラリがあれば記述
    'pyserial',
]

setup(
    name='rs232com',
    version=VERSION,
    description="RS232C communication module",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='Imagenics.co.,ltd',
    license='MIT License',
    keywords='rs232c module',
    python_requires='>=3.6',
    extras_require={
        "docs": ["Sphinx >= 3.4", ],
    },
    packages=find_packages(),
    install_requires=install_requires,
)
