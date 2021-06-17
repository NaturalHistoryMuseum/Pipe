FROM python:stretch

# install OS packages
RUN apt-get update && apt-get install -y --no-install-recommends \
                mysql-client graphviz

# copy project files over to container
COPY . /opt/app
WORKDIR /opt/app

COPY deploy/.jupyter /root/.jupyter

# install python packages
RUN pip install -r deploy/requirements.txt

# get/load data files
RUN python -m spacy download en_core_web_md
RUN python deploy/download_nltk.py
RUN wget -O /usr/local/lib/python3.7/site-packages/epitator/importers/doid_extension.ttl https://github.com/ecohealthalliance/EpiTator/raw/master/epitator/importers/doid_extension.ttl

CMD ["sh", "/opt/app/deploy/entrypoint.sh"]
