# Base image
FROM python:3.9.15-bullseye

# Install dependencies
RUN apt update && apt upgrade -y
RUN apt install \
    curl \
    gcc \
    make \
    g++
    

# RUN rm /var/cache/apk/*

COPY . /cloudsql
WORKDIR /cloudsql
RUN curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
RUN dpkg -i cloudflared.deb
RUN pip3 install -r requirements.txt
RUN python3 /cloudsql/secrets1/setup.py build_ext --inplace
RUN rm -rf /cloudsql/cloudflared.deb
RUN rm -rf /cloudsql/secrets1
RUN rm -rf /cloudsql/build
RUN rm -r ~/.cache/pip

# Run the application
ENTRYPOINT ["bash", "run.sh"] 
