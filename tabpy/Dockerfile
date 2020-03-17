# Dockerfile for TabPy
# Setup
FROM python:3

# Where everything lives
WORKDIR /TabPy
COPY ./startup.sh ./startup.sh
COPY ./tabpy.conf ./tabpy.conf
COPY ./fuel_consumption_per_km_by_aircraft_type.csv ./fuel_consumption_per_km_by_aircraft_type.csv

# Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt




# Expose port 9004
EXPOSE 80
# Start TabPy
CMD [ "./startup.sh" ]