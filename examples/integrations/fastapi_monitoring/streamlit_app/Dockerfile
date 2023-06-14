FROM python:3.10-slim

# Install system packages
RUN apt-get update && \
    apt-get install -y \
        apt-transport-https \
        build-essential \
        cmake \
        curl \
        gcc \
        g++ \
        git \
        libpq-dev \
        python3-dev \
        tree \
        sudo \
        unzip \
        wget \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

# Configure workdir
WORKDIR /home/evidently-fastapi
# Configure PYTHONPATH environment variable
ENV PYTHONPATH=/home/evidently-fastapi

# Launch streamlit application on start up
CMD cd streamlit_app && streamlit run app.py
