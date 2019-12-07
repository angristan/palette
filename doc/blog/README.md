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
