# ASTRiDE (Automated Streak Detection for High Velocity Objects)

This package is the Python version of the streak detection pipeline
originally programmed in C. See details at:
[https://sites.google.com/site/dwkim78/streak-detection](https://sites.google.com/site/dwkim78/streak-detection)

Basic idea is same with the C version, which uses a contour map of a fits image
to detect streaks. Nevertheless, the Python version has an improved algorithm
to determine whether or not the edges (i.e. each contour) 
in the contour map are streak.
For details, see the section "[Algorithm](#6-algorithm)". 

## Index
1. [Dependency](#1-dependency)
2. [Installation](#2-installation)
3. [Test the Installation](#3-test)
4. [How to Use ASTRiDE](#4-pseudo-code-how-to-use-astride)
5. [Algorithm](#5-algorithm)

- [ChangeLog](#changelog)
- [Citation](#citation)

## 1. Dependency

[Python 2.7+](https://www.python.org/) 

 * Not tested with Python 3.0+

[Numpy 1.9+](http://www.numpy.org/)
 
 * Numerical Python library.

[Astropy 1.1.1+](http://www.astropy.org/)

 * For reading fits file and some utility functions.

[Matplotlib 1.5.1+](http://matplotlib.org/)

 * For plotting figures of detected streaks.

[Phoutils 0.2.1+](http://photutils.readthedocs.org/en/latest/index.html)

 * For calculating background map of a fits image.

## 2. Installation

The easiest way to install the ASTRiDE package is:

```python
pip install astride
```

Or,

```python
pip install git+https://github.com/dwkim78/ASTRiDE
```

If you do not want to install/upgrade the dependencies,
execute the above commend with the ```--no-deps``` option.
ASTRiDE possibly works with older version of Python and other libraries. 


Alternatively, you can download the ASTRiDE package from the Git repository as:

```python
git clone https://github.com/dwkim78/ASTRiDE

cd ASTRiDE
python setup.py install
```

You can edit ```setup.py```, if you do not want to update 
your own Python libraries (i.e. edit the ```install_requires``` variable).


## 3. Test

## 4. Pseudo Code: How to Use ASTRiDE? 

## 5. Algorithm

ASTRiDE detects streaks based on the contour of a fits image. ASTRiDE does
not remove sources (e.g. stars) before detecting streaks because source
detection algorithms (e.g. Source Extractor) often detects sources inside a streak.
Thus, rather than removing stars using such source detection methods,
we remove star-like-shaped sources based on the shape of each contour from the image.
For details of the detection procedures, see the following items.

  1. Background removal
    * We use photutils to generate a background map of an input fits image, and
    then subtract the background from the raw image.
  
  2. Contour map
  
  3. Streak detection based on the shape of the contour
  
  4. Connect streaks

## ChangeLog

### v0.2
 - Beta version released. 

### v0.1
 - initiate the GitHub repository.

## Citation