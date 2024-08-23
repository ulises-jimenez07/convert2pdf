FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libreoffice unoconv
# Set up working directory
WORKDIR /app
# Copy application code
COPY . ./
# Install Python dependencies

ENV PORT 8000
RUN pip3 install --no-cache-dir -r requirements.txt

# Start the FastAPI application
CMD exec uvicorn api_pdf_converter:app --host 0.0.0.0 --port 8000