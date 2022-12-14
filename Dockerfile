FROM python:3

RUN apt-get update
RUN apt-get -y install locales && \
  localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get install -y vim

WORKDIR /google_api_product

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "bash" ]
