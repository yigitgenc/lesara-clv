FROM python:3.6-alpine

# Create app user and app directory, set no password for `app` user.
RUN apk update && apk upgrade && apk add --no-cache g++ sudo && \
    mkdir /app && addgroup -g 1337 -S app && adduser -u 1337 -h /app -D -S app -G app  && \
    echo "app ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers

# Get the argument from docker-compose.yml file.
ARG SOURCE_DIR

# Add the files of ${SOURCE_DIR} directory inside the container.
ADD ${SOURCE_DIR} /app

# Create app directory; add `app` (1337) user and group.
RUN chown -R app:app /app && chmod -R g+w /app

# Set working directory.
WORKDIR /app

# Set environmenet variables.
ENV PYTHONBUFFERED 1

# Set user.
USER app

# Install pip packages.
RUN sudo -H pip install --upgrade pip
RUN sudo -H pip install -r requirements.txt
