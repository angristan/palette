# Palette

Palette is a website where you can upload an image and get the dominant colors (using k-means clustering) as well as the associated color names (using k-nearest neighbor).

This is a project for the *Introduction to Artificial Intelligence* at Hanyang University under professor Youngjoon Won.

Motivation, technical details and methodology cam be found in our so-called "[blog post](docs/blog)" as part the [assignment](docs/instructions-assignement-blog-post-video.pdf).

![](docs/images/app.png)


## Setup

Requirements: Python 3

```sh
git clone git@github.com:angristan/palette.git
cd palette
pip install -r requirements.txt
flask run
```

Palette is running on http://localhost:5000/.
