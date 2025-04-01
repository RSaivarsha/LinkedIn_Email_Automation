# Use official Streamlit + Python base
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg \
    chromium-driver \
    chromium \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libappindicator1 \
    libindicator7 \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    --no-install-recommends \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variable for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="$PATH:/usr/lib/chromium"

# Copy app
WORKDIR /app
COPY . .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]
