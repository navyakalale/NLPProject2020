# Ubuntu Linux as the base image
FROM ubuntu:16.04
# Set UTF-8 encoding
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
# Install packages, you should modify this based on your program
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3-pip python3-dev
RUN pip3 install thinc
RUN pip3 install requests
RUN pip3 install spacy
RUN python3 -m spacy download en_core_web_sm
RUN pip3 install nltk
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader averaged_perceptron_tagger
RUN python3 -m nltk.downloader maxent_ne_chunker
RUN python3 -m nltk.downloader words
RUN mkdir /QA/
# Add the files into container, under QA folder, modify this based on your need
ADD ask /QA/
ADD answer /QA/
# Change the permissions of programs, you may add other command if needed
CMD ["chmod 777 ask"]
CMD ["chmod 777 answer"]
# Set working dir as /QA/
WORKDIR /QA/
ENTRYPOINT ["/bin/bash", "-c"]