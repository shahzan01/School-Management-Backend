# Use an official Python runtime as a parent image
FROM python:3.12


# Set environment variables
ENV FLASK_APP=core/server.py
ENV FLASK_ENV=production

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies globally in the container (no virtualenv needed)
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Reset DB
RUN   flask db upgrade -d core/migrations/




# Expose Flask port
EXPOSE 5000
# Set entrypoint to allow passing custom commands
ENTRYPOINT ["bash"]
