========
Blurring
========
Censor videos automatically


Development
-----------

Virtual environment windows::

  python -m venv venv
  venv\Scripts\activate

Virtual environment linux::

  python3 -m venv venv
  source venv/bin/activate

Setup project::

  python -m pip install --upgrade pip wheel setuptools tox flake8 pylama pylint coverage
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
