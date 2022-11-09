FROM python:3.10.4 AS build

ARG UID=1000
ARG GID=1000
ARG UNAME=smartcast_docker
ARG runDeps

ENV VERSION=3.10.4 \
    LANG="C.UTF-8" \
    APP_ROOT="/usr/src/engine" \
    BUNDLE_APP_CONFIG="/usr/src/.vendor/bundle" \
    UNAME=$UNAME \
    PYTHONUNBUFFERED=1

RUN groupadd -g $GID $UNAME && \
    useradd -u $UID -g $UNAME $UNAME

RUN mkdir -p $APP_ROOT && \
    mkdir /home/$UNAME
RUN chmod -R 700 /usr/src && \
    chown -R $UNAME:$UNAME /usr/src && \
    chown -R $UNAME:$UNAME /home/$UNAME

ENV PATH=$PATH:/home/$UNAME/.local/bin

RUN python -m pip install --upgrade pip

USER $UNAME
WORKDIR /usr/src
COPY --chown=$UNAME:$UNAME . /usr/src

RUN pip install --no-cache-dir -r requirements.txt

#FROM build AS test
#RUN pip install -r requirements-dev.txt && rm -rf /home/$UNAME/.cache

#RUN flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
#RUN flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
##  Ensure Test always comply
#RUN flake8 tests/ --count --max-complexity=10 --max-line-length=127 --statistics
#RUN pytest --cov=app --cov-branch --cov-report xml:report/coverage.xml --cov-report term --junitxml=report/tests.xml tests

FROM build AS final