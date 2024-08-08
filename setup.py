from setuptools import setup, find_packages
import os
import shutil

def post_install():
    """Post-installation script to copy the default config."""
    config_source = os.path.join(os.path.dirname(__file__), 'src', 'runmd', 'config.json')
    config_dest = os.path.expanduser('~/.config/runmd/config.json')
    if not os.path.exists(os.path.dirname(config_dest)):
        os.makedirs(os.path.dirname(config_dest))
    if not os.path.exists(config_dest):
        shutil.copy(config_source, config_dest)

setup(
    name='runmd',
    version='0.1.0',
    package_dir={'': 'src'},  # Tell setuptools to look for packages in the src directory
    packages=find_packages(where='src'),  # Find packages in src
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'runmd = runmd.cli:main',  # Adjusted to the new module path
        ],
    },
    description='A CLI tool to run or list code blocks from Markdown files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/yourproject',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    data_files=[
        ('~/.config/runmd', ['src/runmd/config.json']),
    ],
)

# Execute post-installation tasks
post_install()
