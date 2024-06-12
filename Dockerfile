FROM python:3.10.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /opt
ENV POETRY_VIRTUALENVS_CREATE=false
ENV QT_DEBUG_PLUGINS=1

ENV DEBIAN_FRONTEND=noninteractive
# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

RUN apt-get update && apt-get install -y build-essential git python3-pip python3-dev libldap2-dev libsasl2-dev ruby python3-pyqt5 ruby
ENV PATH "${PATH}:/root/.gem/ruby/2.7.0/bin:/root/.local/share/gem/ruby/2.7.0/bin"
RUN echo $PATH
RUN gem install fpm --user-install

RUN pip install pip==23.0.1 poetry

RUN which gem
RUN export ALINKA_VERSION=`poetry version --short`
RUN export INSTALLER_FILE_NAME="alinka-${ALINKA_VERSION}.deb"

RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser
RUN mkdir /opt/app
WORKDIR /opt

COPY ./app /opt/app
COPY ./pyproject.toml /opt/pyproject.toml
COPY ./poetry.lock /opt/poetry.lock

RUN poetry install --no-interaction --with dev
