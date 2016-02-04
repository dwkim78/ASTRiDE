from setuptools import find_packages, setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='astride',
    version='0.1',
    description='Automated Streak Detection for High Velocity Objects',
    long_description=readme(),
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/dwkim78/astride',
    license='MIT',
    author='Dae-Won Kim',
    author_email='dwkim78@gmail.com',
    install_requires=['numpy>=1.9',],
    keywords=['astronomy', 'image', 'light curves', 'streak'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Astronomy'
    ]
)
