FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

# install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y wget unzip libnss3 && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["python", "devtoblog.py"]