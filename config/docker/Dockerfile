FROM python:3.9 as base
RUN apt update
RUN apt install -y libmemcached-dev
RUN apt install -y gettext

RUN apt-get install -y \
  --fix-missing automake build-essential \
  curl \
  libffi-dev \
  libssl-dev \
  gdal-bin \
  libgdal-dev \
  python3-gdal \
  binutils \
  libproj-dev \
  ssh \
  screen \
  vim \
  less \
  postgresql-client

RUN \
  # Clean up
  apt-get remove -y automake curl build-essential && \
  apt-get autoremove -y && \
  apt-get autoclean && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN mkdir /logs
RUN mkdir /webroot
RUN mkdir -p /opt/edlight
RUN chmod 0777 /opt/edlight

FROM base as base_python
ENV PIPENV_PIPFILE=/opt/edlight/Pipfile
COPY ./Pipfile /opt/edlight/Pipfile
COPY ./Pipfile.lock /opt/edlight/Pipfile.lock
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system
# deal with pipenv not installing from a repository for systems
# RUN pip install git+https://github.com/castlabs/pycaption.git@master#egg=pycaption


COPY . /opt/edlight
WORKDIR /opt/edlight
