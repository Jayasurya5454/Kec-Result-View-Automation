
FROM python:3.9


RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
 && rm -rf /var/lib/apt/lists/*

ENV CHROMEDRIVER_VERSION 92.0.4515.107

RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip -d /usr/local/bin/

# Set display port to avoid crash
ENV DISPLAY=:99

# Set environment variable to run Streamlit in headless mode
ENV STREAMLIT_SERVER_HEADLESS true

# Copy app files
COPY . /app
WORKDIR /app

# Install app dependencies
RUN pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py"]
