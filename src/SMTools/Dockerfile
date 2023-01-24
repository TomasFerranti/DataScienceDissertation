FROM python:3.8-slim

# Opencv requirements
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

# Matplotlib requirements
RUN apt-get install python3-tk -y

# Upgrade pip
RUN python -m pip install --upgrade pip

# Set workdir name
WORKDIR /SMTools

# Install pip requirements
COPY app/requirements.txt .
RUN python -m pip install -r requirements.txt

# Start app
WORKDIR /SMTools/app
CMD ["tail", "-f", "/dev/null"]