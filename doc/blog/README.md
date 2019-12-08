# Image color palette extraction for color-blinded people

## Team

*All the members are from the Department of Computer Science at Hanyang University (South Korea)*

- Ni Putu Winda Ardiyanti
- Asty Nabilah Izzaturrahmah
- Stanislas Lange (angristan@pm.me)
- Stephane Rabenarisoa

## I. Introduction

- Motivation: Why are you doing this? - What do you want to see at the end?

The goal of our project is to help color-blinded people trough our service.

According to [Wikipedia](https://en.wikipedia.org/wiki/Color_blindness):

> Color blindness, also known as color vision deficiency, is the decreased ability to see color or differences in color.

Our service is a website available for free where users can upload a picture, and from that picture get the major tints of an image. The human ability to recognize colors is not absolute and can be tricked trough the use of tints. Color recognition is even harder for color blinded people, thus we want to help them by giving them the dominant color of an image, also known as color palette.

To achieve this, we use multiple algorithms. The first one will extract the major colors from an image (the number of colors is configurable), and it will return them as hexadecimal or RGB values (see below for RGB). The second one will associate the color values with the closest color name in English for each color.

## II. Datasets
- Describing your dataset

### Extracting colors: converting an image into a usable dataset

To analyze the colors of an image, we only need the image itself, which we can consider as our dataset. As we explain in `III.`, we use the k-means clustering algorithm for this matter.

An image can be broken down into a two dimensional array for pixels, defined by its height and width, in pixels. Each pixel itself is a 3 dimensional array with a red, green and blue (RGB) value.

The RGB color model is an additive color model in which red, green, and blue light are added together in various ways to reproduce a broad array of colors.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/RGB_color_solid_cube.png/640px-RGB_color_solid_cube.png?download)

*3D representation of a RGB pixel*

The RGB24 model is composed of 3 color channel each holding 8 bits of data, a value from 0 to 255 according to the amount of that specific color in the channel. Each pixel holds a total of 24 bits.


![](https://www.researchgate.net/profile/Jane_Courtney2/publication/267210444/figure/fig6/AS:295732335661069@1447519491773/A-three-dimensional-RGB-matrix-Each-layer-of-the-matrix-is-a-two-dimensional-matrix.png)

*Image represented as 3D matrix. Each layer is a color channel represented as a 2D matrix.*

24 bits is 256<sup>3</sup>. With this system, 16,777,216 (256<sup>3</sup> or 2<sup>24</sup>) discrete combinations of R, G, and B values are allowed, providing millions of different (though not necessarily distinguishable) hue, saturation and lightness shades, which results in different colors, or tints.

![](https://i.imgur.com/QzK05y0.png)

*Images with pixels of different bit depth also known as color depth. The standard is 24-bits.*

There are other color models but the second most popular is the CMY color model (for Cyan, Magenta and Yellow), which is a subtractive color model as opposed to RGB which is additive.

To extract the dominant colors from an image we don't care about the placement of the pixels in the image, but only their color. Thus we can convert the image into an array of RGB values.

Let's take this image as a example:

![](https://i.imgur.com/8EfDXN1.png)

*3x3 image*

This image is our dataset, and we will prepare it for our clustering algorithm.

We use OpenCV in Python to manipulate the image:

```py
import cv2
```

When reading a color image file, OpenCV `imread()` reads as a NumPy array `ndarray` of row (height) x column (width) x color (3). The order of color is BGR (blue, green, red). So we have to convert it to RGB.

```py
img = cv2.imread('3x3.png')

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

If we `print(img)` now we will have a 3D array as expected:

```py
[[[255   0   0]
  [255   0   0]
  [255   0   0]]

 [[  0 255   0]
  [  0 255   0]
  [  0 255   0]]

 [[  0   0 255]
  [  0   0 255]
  [  0   0 255]]]
```

Since we don't care about the pixel placement we can convert the image to a 2D array, which can be seen as reshaping the image from 3x3 pixels to 1x9 pixels.

```py
img = img.reshape((img_data.shape[0] * img_data.shape[1], 3))
```

Now by issuing `print(img)` we can attest that we have prepared our image for the clustering.

```py
[[  0   0 255]
 [  0   0 255]
 [  0   0 255]
 [  0 255   0]
 [  0 255   0]
 [  0 255   0]
 [255   0   0]
 [255   0   0]
 [255   0   0]]
```

### Associating color values with color names

With the methodology described below we extract a certain number of dominant colors as RGB or Hexadecimal values. Since this not something that will help our user (what's the good of knowing that `123,43,234` is the dominant tint in an image?), we have to provide them with a name corresponding to each color.

To that end we use a CSV dataset available [here](../../dataset/wikipedia_color_names.csv) containing 1298 colors.

Here is an extract:

```csv
"name","hex","red","green","blue","hue","hsl_s","hsl_l, hsv_s, hsv_v"
"Absolute zero","#0048BA",0,72,186,217.0,100.0,37.0
"Acid green","#B0BF1A",176,191,26,65.0,76.0,43.0
"Aero","#7CB9E8",124,185,232,206.0,70.0,70.0
"Aero blue","#C9FFE5",201,255,229,151.0,100.0,89.0
"African violet","#B284BE",178,132,190,288.0,31.0,63.0
```

That dataset originally comes from [Wikipedia (List of colors)](https://en.wikipedia.org/wiki/Lists_of_colors) and has been converted to CSV by Dilum Ranatunga and published on [data.world](https://data.world/dilumr/color-names).

We need to import and prepare that dataset because we only need the first four columns in the CSV file.

To do so we use the [pandas]() library.

```py
import pandas as pd
```

First we convert the CSV file to a `pandas.core.frame.DataFrame` object to easily extract data.

```py
data = pd.read_csv("wikipedia_color_names.csv")
```

We can verify the import with the `data.head()` method:

```py
             name      hex  red  green  blue    hue  hsl_s  hsl_l, hsv_s, hsv_v
0   Absolute zero  #0048BA    0     72   186  217.0  100.0                 37.0
1      Acid green  #B0BF1A  176    191    26   65.0   76.0                 43.0
2            Aero  #7CB9E8  124    185   232  206.0   70.0                 70.0
3       Aero blue  #C9FFE5  201    255   229  151.0  100.0                 89.0
4  African violet  #B284BE  178    132   190  288.0   31.0                 63.0
```

Then we extract the name and RGB values into 4 variables.

```py
color_names = data['name'].tolist()
r = data['red'].tolist()
g = data['green'].tolist()
b = data['blue'].tolist()
```

We are careful to keep the order of the data when converting them to list, otherwise the colors will be mixed.

Now that we have extracted the data we needed, we will be able to use it for our classifying algorithm below.

## III. Methodology

- Explaining your choice of algorithms (methods) - Explaining features or code (if any)
- until Dec. 17

### Code architecture: how we built the website with Flask

- Flask + Jinja
- Frontend JS + API
- Bootstrap
- Heroku with GitHub Actions

### Extracting colors: k-means clustering

### Classifying colors: k-nearest neighbors

## IV. Evaluation & Analysis

- Graphs, tables, any statistics (if any)

## V. Related Work (e.g., existing studies)

- Tools, libraries, blogs, or any documentation that you have used to do this project.

## VI. Conclusion: Discussion
