# Dockerfile for TabPy
# Setup - take the latest version of Python 3 from the officil image
FROM python:3

# Where everything lives
WORKDIR /TabPy

# Copy every file you need to your working directory
COPY ./startup.sh ./startup.sh
COPY ./tabpy.conf ./tabpy.conf

# Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 9004 - decide what port should docker make available for this container
EXPOSE 9004
# Start TabPy
CMD [ "./startup.sh" ]