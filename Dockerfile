FROM python:3 AS build

ENV PATH=$PATH:/home/$UNAME/.local/bin

RUN python -m pip install --upgrade pip
WORKDIR /code
RUN chown $UNAME:$UNAME /code
USER $UNAME

COPY --chown=$UNAME:$UNAME requirements.txt /code/

RUN pip install --no-cache-dir -r /code/requirements.txt
COPY --chown=$UNAME:$UNAME ./ /code/

FROM build AS test
RUN pip install -r requirements-dev.txt && rm -rf /home/$UNAME/.cache

# RUN flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
# RUN flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
#  Ensure Test always comply
# RUN flake8 tests/ --count --max-complexity=10 --max-line-length=127 --statistics
# RUN pytest --cov=src --cov-branch --cov-report xml:report/coverage.xml --cov-report term --junitxml=report/tests.xml tests

FROM build AS final

# COPY --from=test /code/report/tests.xml ./