# Color palette extraction from an image for color-blinded people

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

Our service is a website available for free where users can upload a picture, and from that picture get the major tints of an image. The human ability to recognise colors is not absolute and can be tricked trough the use of tints. Color recognition is even harder for color blinded people, thus we want to help them by giving them the dominant color of an image, also known as color palette.

To achieve this, we use multiple algorithms. The first one will extract the major colors from an image (the number of colors is configurable), and it will return them as hexadecimal or RGB values (see below for RGB). The second one will associate the color values with the closest color name in English for each color.

## II. Datasets
- Describing your dataset

To analyse the colors of an image, we only need the image itself, which we can consider as our dataset. As we explain in `III.`, we use the k-means clustering algorithm for this matter.

An image can be broken down into a two dimensional array for pixels, defined by its height and width, in pixels. Each pixel itself is a 3 dimentional array with a red, gree and blue (RGB) value.

The RGB color model is an additive color model in which red, green, and blue light are added together in various ways to reproduce a broad array of colors.

This 3D model can be visualised as this cube:

![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/RGB_color_solid_cube.png/640px-RGB_color_solid_cube.png?download)

The RGB24 model is composed of 3 color channel each holding 8 bits of data, a value from 0 to 255 according to the amount of that specific color in the channel. Each pixel holds a total of 24 bits.

24 bits is 256<sup>3</sup>. With this system, 16,777,216 (256<sup>3</sup> or 2<sup>24</sup>) discrete combinations of R, G, and B values are allowed, providing millions of different (though not necessarily distinguishable) hue, saturation and lightness shades, which results in different colors, or tints.

## III. Methodology
- Explaining your choice of algorithms (methods) - Explaining features or code (if any)
- until Dec. 17

## IV. Evaluation & Analysis
- Graphs, tables, any statistics (if any)

## V. Related Work (e.g., existing studies)
- Tools, libraries, blogs, or any documentation that you have used to do this project.

## VI. Conclusion: Discussion
