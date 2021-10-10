from setuptools import setup, find_packages

setup(
    name='group_mv',
    version='0.0.1',
    author='Robert Walz',
    author_email='robertwalz35@gmail.com',
    url='https://github.com/rbrtwlz/group_mv.git',
    description='program to archive files',
    packages=["group_mv"],    
	py_modules=['main', 'logger', 'utils'],
	entry_points = {
		    'console_scripts' : ['group_mv = group_mv.main:main']
	},
    install_requires = []
)
