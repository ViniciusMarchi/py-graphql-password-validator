FROM python:3.10-slim-buster
# create a directory named /app
WORKDIR /app
# copy the file that list the project's dependencies
COPY requirements.txt requirements.txt
# updates OS running in container
RUN apt update
# update pip
RUN pip install --upgrade pip
# download and install the necessary dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
# copy the api code
COPY . .
EXPOSE 8000
# run api
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]