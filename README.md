# ASTRiDE (Automated Streak Detection for High Velocity Objects)

This package is the Python version of the streak detection pipeline
([Kim+ 2005](http://adsabs.harvard.edu/abs/2005JASS...22..385K) and 
[https://sites.google.com/site/dwkim78/streak-detection](https://sites.google.com/site/dwkim78/streak-detection))
originally programmed in C.

Basic idea is same with the C version, which uses a contour map of a fits image
to detect streaks. Nevertheless, the Python version has an improved algorithm
to determine whether each edge (i.e. each contour) 
in the contour map is a streak or not
For details, see the section "[How to Use ASTRiDE](#4-how-to-use-astride)". 

## Index
1. [Dependency](#1-dependency)
2. [Installation](#2-installation)
3. [Test the Installation](#3-test)
4. [How to Use ASTRiDE](#4-how-to-use-astride)
5. [Test with Crowded Field Image](#5-test-with-crowded-field-image)

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

To check if ASTRiDE is correctly installed, type following commands in 
your Python console.

```python
from astride import test

test()
```

The command will print messages like:
```
2016-02-15 16:16:18,239 INFO - Start.
2016-02-15 16:16:18,241 INFO - Read a fits file..
2016-02-15 16:16:18,272 INFO - Search streaks..
2016-02-15 16:16:19,027 INFO - Save figures and write outputs to ./long/
2016-02-15 16:16:20,048 INFO - Done.
```

The test module will also save figures and write information of detected 
streaks under the "./long/" folder. In the folder, you can find two images
and one text file. The two images are:

| Image name | Description |
|----:|:------------|
| all.png |  An entire fit image with detected streak (shown below) |
| 1.png | A zoomed image for each linked streak |

<div align="center">
<img src="https://github.com/dwkim78/ASTRiDE/blob/master/astride/datasets/images/all.png">
[ all.png ]</div>


The output text file named as "streak.txt" contains following information.

| Column | Description |
|----:|:------------|
| ID  | Index |
| x_center, y_center  | Coordinate of the center  |
| area  | Area inside a streak  |
| perimeter  | Length of perimeter of a streak  |
| shape_factor  | 4 * PI * 'area' / 'perimeter'^2 |
| radius_deviation  | Parameter to check roundness  |
| slope  | Slope of a linear line fitted to a streak  |
| intercept  | Intercept of a linear line fitted to a streak  |
| connectivity  | ID of another streak that is likely to be linked to the current streak  |


I will explain details about the figures and the text file in the following section.


## 4. How to Use ASTRiDE? 

In this section, I will show how to use ASTRiDE to detect streak. I will use
the fits image shown in the previous section (i.e. all.png).

### Create STREAK Instance

We first need to create ASTRiDE Streak instance as:

```python
from astride import Streak

streak = Streak('long.fits')
```

There are many options customizing the Streak instance such as:

| Options | Description |
|----:|:------------|
| bkg_box_size  | A box size for calculating a background map of a fits image |
| contour_threshold  | A threshold to extract a contour map |
| min_points  | The minimum number of data points in each contour in the contour map
| shape_cut  | An empirical cut for shape factor |
| area_cut | An empirical cut for area inside each contour |
| radius_dev_cut  | An empirical cut for radius deviation |
| connectivity_angle | The maximum angle to link each edge |
| output_path  | An output path to save figures and outputs |

Although you can customize pretty much all of the Streak instance, I recommend
to leave them as they are.


### Detect Streaks

We can now detect streaks in the fits image as:

```python

streak.detect()
```

In order to detect streaks, the Streak instance does as follows:

  1. Background removal
    * We use photutils to generate a background map of an input fits image, and
    then subtract the background from the raw image.
  
  2. Contour map
  
  3. Streak detection based on the shape of the contour
  
  4. Connect streaks

### Note

As you might notice, ASTRiDE does
not use any source detection algorithm (e.g. Source Extractor) to distinguish
stars from streaks. This is because such algorithms often find stellar-like-sources
<b>inside</b> a streak. For instance, see the following figure.

<div align="center">
<img src="https://github.com/dwkim78/ASTRiDE/blob/master/astride/datasets/images/source_detection.png">
[ Source Detection ]</div>

Thus we cannot use such source detection algorithms to remove stars before 
detecting streaks. One could think of using each detected source to
detect streaks by somehow connecting them. Such method, however, would not
be successful either for 1) short streaks, or 2) crowded field.


### 5. Test with Crowded Field Image


### Logger

If you want to write log messages either to console or to disk, 
you can use the ASTRiDE Logger class as:

```python
from astride import Logger

logger = Logger().getLogger()

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```

Keep in mind that you need to generate only one logger instance 
through the whole processes, but not many.
If you want to save log messages to a file, 
generate a logger instance as follows:
 
 ```python
 logger = Logger('/PATH/TO/FILE.log').getLogger()
 ```

This will send log messages to both console and a log file.
Note that the path must be the absolute path.

## ChangeLog

### v0.2
 - Beta version released. 

### v0.1
 - initiate the GitHub repository.

## Citation