FROM python:3-slim

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install -r requirements.txt

# Bundle app source
COPY . .

EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]
