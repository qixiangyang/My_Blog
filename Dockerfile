FROM python:3.7.5

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo 'Asia/Shanghai' >/etc/timezone

RUN apt-get update && apt-get install -y libsasl2-dev \
libldap2-dev \
libssl-dev

WORKDIR /my_blog

COPY ./requirements.txt /my_blog
RUN pip install -r requirements.txt

COPY . /my_blog

ENV FLASK_APP my_blog.py
ENV FLASK_ENV production

ENTRYPOINT ["./entrypoint.sh"]
