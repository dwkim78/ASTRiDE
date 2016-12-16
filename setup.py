from setuptools import find_packages, setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='astride',
    version='0.3.1',
    description='Automated Streak Detection for High Velocity Objects',
    long_description=readme(),
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/dwkim78/astride',
    license='MIT',
    author='Dae-Won Kim',
    author_email='dwkim78@gmail.com',
    install_requires=['numpy>=1.11.2', 'photutils>=0.3', 'astropy>=1.2',
                      'matplotlib>=1.5.3', 'scipy>=0.18.1',
                      'scikit-image>=0.12.3'],
    keywords=['astronomy', 'image', 'streak', 'satellite', 'meteor', 'NEO',
              'fast-moving objects', 'boundary-tracing', 'contour-tracing'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Astronomy'
    ]
)
