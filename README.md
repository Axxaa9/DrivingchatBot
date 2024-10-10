## GenDrive project
full name of the project: Generative AI-powered Vehicle Personalization and Predictive Maintenance System

## requirements

- python 3.9 or later

### Install Python using Anaconda

1) Download and install Anaconda from [here](https://docs.anaconda.com/free/anaconda/install/index.html)
2) Create a new environment using the following command:
```bash
$ conda create -n GenDrive python=3.9
```
3) activate the environment:
```bash
$ conda activate GenDrive
```
## (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ cd src
$ pip install -r requirements.txt
```

### setup the environment 

```bash
$ cp .env.example .env
```

Set your environment in the `.env` file. Like `OPEN_API_KEY` value.

## Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```
## for first time run docker

```bash
$ docker-compose up -d
```
## to start docker 

```bash
$ docker-compose start
```

## Run the FastAPI server (be in the src directory)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
