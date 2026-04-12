FROM python:3.9-slim

WORKDIR /app

# Ensure we have the latest pip
RUN pip install --no-cache-dir --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Hugging Face Spaces runs containers as a non-root user (UID 1000).
# We must ensure this user has the necessary permissions to write to uploads and databases.
RUN useradd -m -u 1000 user
RUN mkdir -p /app/uploads
RUN chown -R user:user /app

# Switch to the non-root user
USER user

# Set the environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Hugging Face exposes port 7860 by default
EXPOSE 7860

# Use gunicorn as the production WSGI server
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
