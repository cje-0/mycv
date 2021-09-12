FROM python:bullseye
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8
RUN apt-get update && apt-get install -y --no-install-recommends texlive texlive-pictures texlive-latex-extra texlive-fonts-extra

WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .
COPY ./example-data ./data
COPY ./src/mycv-version.txt /mycv-version.txt

CMD [ "python", "./cv.py" ] 
