======================================
Blurring - censor videos automatically
======================================
.. image:: https://img.shields.io/pypi/v/blurring
   :alt: PyPI
   :target: https://pypi.org/project/blurring/

.. image:: https://img.shields.io/pypi/pyversions/blurring
   :alt: Python Version
   :target: https://pypi.org/project/blurring/

.. image:: https://img.shields.io/pypi/l/blurring
   :alt: License
   :target: https://pypi.org/project/blurring/

I use a simple template match to find the secret spots in the video. So this is
nothing for a dynamical video. It should be used to clean up for screen records.

Why
---
Blurring is designed to expand `Watch me Coding <https://github.com/axju/wmc>`_.
I take my screen in time lapse. One second, one frame. That's 3600 frames for
an hour. An 8-hour coding day would be 28800 frames. I do not want to search
for secret information in every single frame. I know my secret passwords so I
can scan the video and blur them.

Install
-------
Simple as always. Do not forget to use a virtual environment::

  >>> pip install blurring

How to uses
-----------
Create a template. You can use any image. Maybe something created with gimp. Or
us supplied tool "blurring-t" (I know that is a ugly name, sorry)::

  >>> blurring-t template
  text [PASSWORD]: PASSWORD
  height [18]: 18
  ...

Before you blur the video, checkout the original.

.. image:: https://github.com/axju/blurring/blob/develop/ext/video.gif?raw=true
   :alt: alternate text
   :align: right

Now blur it. I use the offset to blur the password before it is completely
visible::

  blurring video.mp4 blurred.mp4 template.png --offset 60

This is the result.

.. image:: https://github.com/axju/blurring/blob/develop/ext/blured_60.gif?raw=true
   :alt: alternate text
   :align: right

And this would be the result without the offset.

.. image:: https://github.com/axju/blurring/blob/develop/ext/blured_0.gif?raw=true
   :alt: alternate text
   :align: right

There is still something to improve, but for now I am happy.


Watch me coding integration
---------------------------
This is also a plugin for watch me encoding. After you have installed Blurring,
there is an additional command::

  >>> wmc -H
          info v0.3.3 - Print some infos
          link v0.3.3 - Concat all videos to one
        record v0.3.3 - Start the record
         setup v0.3.3 - Setup the project
      blurring v0.1.0 - Blur the final video

First create the final video::

  >>> wmc link

Now create the template(s)::

  >>> mkdir templates
  >>> blurring-t templates/dummy
  text [PASSWORD]: PASSWORD
  height [18]: 18
  width [70]: 70
  scale [0.4]: 0.4
  font [0]: 0
  pos_x [0]: 0
  pos_y [12]: 12

It is time to blurring out the "PASSWORD"::

  >>> wmc blurring

Now you have the video "full_blur.mp4". Enjoy it.


Development
-----------
Virtual environment windows::

  python -m venv venv
  venv\Scripts\activate

Virtual environment linux::

  python3 -m venv venv
  source venv/bin/activate

Setup project::

  python -m pip install --upgrade pip wheel setuptools tox flake8 pylama pylint coverage rstcheck
  python setup.py develop

Run some test::

  tox
  pylama src/blurring
  python setup.py test
  python setup.py flake8
  python setup.py check

Test coverage::

  coverage run --source src/blurring setup.py test
  coverage report -m

Publish package::

  git tag -a 1.0.0a1 -m '1.0.0a1'
  rstcheck README.rst
  python setup.py --version
  python setup.py check
  python setup.py sdist bdist_wheel
  twine upload dist/*
  git push origin 1.0.0a1

Create gif's::

  ffmpeg -i ext/blured_60.mp4 -filter_complex "[0:v] palettegen" palette.png
  ffmpeg -i ext/blured_60.mp4 -i palette.png -filter_complex "[0:v][1:v] paletteuse" ext/blured_60.gif
