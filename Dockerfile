FROM python:3.6-slim

RUN apt-get update && apt-get install -y gcc unixodbc-dev libpq-dev wget xz-utils libfontconfig1 libxrender1 libxext6
RUN cd ~ && \
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz && \
tar vxf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz && \
cp wkhtmltox/bin/wk* /usr/local/bin/

RUN mkdir -p app
WORKDIR /app

# add and install requirements
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . .

CMD gunicorn -b 0.0.0.0:5000 --reload "praylink:app"