from setuptools import setup, find_packages


setup(
    name="webdep",
    author="Nathan Klapstein",
    author_email="nklapste@ualberta.ca",
    version="0.0.0",
    description="A simple redeployable cherrypy server with goodies",
    url="https://github.com/nklapste/webdep",
    download_url="",
    packages=find_packages(),
    package_data={
        '': ['README.md', 'LICENSE'],
        'webdep': ['logs/*', 'public/*', 'webpages/*']
    },
    install_requires=[
        "cherrypy",
        "jinja2"
    ],
    entry_points={
        'console_scripts': ['start-server = webdep.__main__:main'],
    },
)