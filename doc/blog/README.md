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

To do so we use the [pandas](https://pandas.pydata.org/) library.

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

To explain why we chose k-means for our project we have to go back to what we try to achieve. After processing our image as explained above, we want to extract `x` dominant colors. However as we saw earlier using the RGB 24-bits color model we has 16,777,216 (256<sup>3</sup> or 2<sup>24</sup>) different colors, most of which being slightly different tints.

To understand the extent of the spectrum, let's look at this rough example:

![](https://i.imgur.com/CWYX7iD.png)

One would classify both of these color as blue, right? The second color has +100 to each color channel, so that means there is 100<sup>3</sup> = 1 million tints between these two blue colors!

To be specific, if we want the *most present colors* in an image, we could do a simple statistical analysis of the RGB values of all the pixels. But the result would be extremely difficult to interpret, because an image of a blue sky can contain a million different tints of blue and be made of unique pixels, thus without any *exact* dominant color.

![](https://miro.medium.com/max/1370/1*pxlI1gPzYHE0ZVaTsg3n2w.png)

*This image is clearly blue, but a statistical analysis would not be as decisive.*

But that's not how humans perceive colors. According to [Deane Brewster Judd and Günter Wyszecki in their book *Color in Business, Science and Industry* published in 1975](https://en.wikipedia.org/wiki/Color_vision#cite_note-business-21), humans can perceive about 10 millions colors. But humans can't tell the difference between very slight tints differences.

Consequently, we want our service to group close tints as a single color. For example if we want to extract the two dominant colors of a landscape image with a blue sky and green grass, our service should group all the tints of blue in the sky as a single blue color and all the tints of green in the grass as a single green color.

In order to achieve this programmatically, we have to use **clustering**.

Clustering is a Machine Learning technique that involves the grouping of data points. Given a set of data points, we can use a clustering algorithm to classify each data point into a specific group. In theory, data points that are in the same group should have similar properties and/or features, while data points in different groups should have highly dissimilar properties and/or features. Clustering is a method of unsupervised learning and is a common technique for statistical data analysis used in many fields.

An **unsupervised learning** method is a method in which we draw references from datasets consisting of input data without labeled responses. Generally, it is used as a process to find meaningful structure, explanatory underlying processes, generative features, and groupings inherent in a set of examples.

There are multiple types of clustering algorithm. But k-means is the easiest to implement and use, and our data is simple enough and well distributed enough (generally) that k-means will be able to clusterize correctly the data, most of the time.

So, how does k-means work?

1. To begin, we first select a number of classes/groups (later called clusters) to use and randomly initialize their respective center points, called centroids. To figure out the number of classes to use, it’s good to take a quick look at the data and try to identify any distinct groupings.

2. Each data point is classified by computing the distance between that point and each group center, and then classifying the point to be in the group whose center is closest to it.

3. Based on these classified points, we recompute the group center by taking the mean of all the vectors in the group.

4. Repeat these steps for a set number of iterations or until the group centers don’t change much between iterations. You can also opt to randomly initialize the group centers a few times, and then select the run that looks like it provided the best results.

![](https://shabal.in/visuals/kmeans/left.gif)

*The centroids are chosen to be the 4 points of the left, and then they are recomputed trough each iteration.*

![](https://stanford.edu/~cpiech/cs221/img/kmeansViz.png)

*A sequential visualisation of k-means*

K-Means has the advantage that it’s pretty fast, as all we’re really doing is computing the distances between points and group centers; very few computations! It thus has a linear complexity O(n).

On the other hand, K-Means has a couple of disadvantages. Firstly, you have to select how many groups/classes there are.

This isn’t always trivial and ideally with a clustering algorithm we’d want it to figure those out for us because the point of it is to gain some insight from the data. However in our case we decided that we want the user to provide the number of dominant colors they want to extract from the image, so it's all good.

![](https://lh3.googleusercontent.com/-PC1vPUvCsKQ/WsjySpfx6uI/AAAAAAAABR8/gF5H-otSOtkAiY7HJUDoxv1HUDvBNtJ7QCLcBGAs/s640/data3d.gif)

*In our case, are data points are three-dimensional (RGB) so the clustering process would look like this.*

K-means also starts with a random choice of cluster centers and therefore it may yield different clustering results on different runs of the algorithm. Thus, **the results may not be repeatable and lack consistency**. K-means is **not deterministic**. Other cluster methods are more consistent.
K-Medians is another clustering algorithm related to K-Means, except instead of recomputing the group center points using the mean we use the median vector of the group. This method is less sensitive to outliers (because of using the Median) but is much slower for larger datasets as sorting is required on each iteration when computing the Median vector.

![](https://datasciencelab.files.wordpress.com/2014/01/kpp_n200_k31.png)

*The choice of initial centroids can lead to completely different and wrong results*

As shown below, even if the random initialization of centroids will lead to corrects results most of the time, it can sometimes completely mess up the clustering.

To overcome the above-mentioned drawback we use K-means++. This algorithm ensures a smarter initialization of the centroids and improves the quality of the clustering. Apart from initialization, the rest of the algorithm is the same as the standard K-means algorithm. That is K-means++ is the standard K-means algorithm coupled with a smarter initialization of the centroids.

The steps involved are:

1. Randomly select the first centroid from the data points.
2. For each data point compute its distance from the nearest, previously chosen centroid.
3. Select the next centroid from the data points such that the probability of choosing a point as centroid is directly proportional to its distance from the nearest, previously chosen centroid. (i.e. the point having maximum distance from the nearest centroid is most likely to be selected next as a centroid)
4. Repeat steps 2 and 3 until k centroids have been sampled

By following the above procedure for initialization, we pick up centroids which are far away from one another. This increases the chances of initially picking up centroids that lie in different clusters.

![](https://www.salientiastuff.com/images/k-means/five_kplusplus.png)

*With this dataset, we can expect that by using k-means++ initialization, the initial centroids will be roughly associated with the apparent clusters nearly all the time, whereas the probability of this happening with the random initialization is much lower.*

Since this is a easy improvement for k-means, we decided to use the k-means++ initialization method over the default, random one. Moreover, this method is available natively in the library we use.

Let's run trough our usage of k-means in Python. Since Python is blessed with excellent Machine Learning libraries such as [scikit-learn](https://scikit-learn.org/stable/), we did not have to re-implement k-means from scratch, although it is possible to be done in a [few dozen lines of code](https://github.com/pavankalyan1997/Machine-learning-without-any-libraries/blob/master/2.Clustering/1.K_Means_Clustering/Kmeans.py) since the algorithm itself is pretty trivial.

```py
from sklearn.cluster import KMeans
```

Let's start by initializing k-means and our model:

```py
k = 3
model = KMeans(n_clusters = k,
                init = 'k-means++',
                n_jobs = -1,
                n_init = 10,
                max_iter = 300,
                algorithm='auto')
```

In the real application we get `k` from the API, but for simplicity here we will use `k=3` as the number of clusters, which means the number of centroids, so number of colors to extract.

As explained above, we use k-means++ as our initialization method, the two other supported being random and a defined set of points as a `ndarray`.

`n_jobs = -1` means we will use all the available CPU cores instead of 1. `n_init` is the number of time the k-means algorithm will be run with different centroid seeds. The final results will be the best output of n_init consecutive runs in terms of inertia. `max_iter` is the maximum number of iterations of the k-means algorithm for a single run.

Then we compute our clusters using our transformed array image:

```py
model.fit(img)
```

This will take from a few milliseconds to a few seconds depending on the image size, the number of clusters and other parameters above such as the number of iterations.

If we take our simple 3x3 image example from earlier:

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

And compute its centroids (3), we get, as expected, red, green, and blue:

```py
print(model.cluster_centers_.astype(int))
```

```py
[[255   0   0]
 [  0 255   0]
 [  0   0 255]]
```

Now, with 2 clusters, we get purple and green:

```py
[[127   0 127]
 [  0 255   0]]
```

And with 4, red, green, blue and blue:

```py
 [[255   0   0]
 [  0 255   0]
 [  0   0 255]
 [  0   0 255]]
```

That helps showing the importance in the number of clusters, however the effect is amplified by the fact that our dataset here is extremely small. In a real image, k-means would give more real tints.

For example, a picture of a blue sky and `k=1` will give use some blue color. But with `k=2`, we will get a light blue and dark blue.

### Classifying colors: k-nearest neighbors

## IV. Evaluation & Analysis

- Graphs, tables, any statistics (if any)

## V. Related Work (e.g., existing studies)

- Tools, libraries, blogs, or any documentation that you have used to do this project.

## VI. Conclusion: Discussion
