FROM python:3.8-slim

# Opencv requirements
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

# Matplotlib requirements
RUN apt-get install python3-tk -y

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Set workdir name and copy content
WORKDIR /SMTools
COPY . .

# Start app
CMD python interface.py