# Use the official ubi minimal base image
FROM registry.access.redhat.com/ubi9/ubi-minimal

# Install python
RUN microdnf install python -y

# Set environment variables
ENV LISTEN_ADDRESS=0.0.0.0
ENV LISTEN_PORT=8443
ENV TLS_CERT_PATH=/var/run/secrets/getpublickey-serving-cert/tls.crt
ENV TLS_KEY_PATH=/var/run/secrets/getpublickey-serving-cert/tls.key

# Set the working directory
WORKDIR /app

# Copy the application source to the container
COPY ./src/getpublickey.py /app/

# Expose the specified port
EXPOSE 8443

# Command to run the server
CMD python ./getpublickey.py --listen $LISTEN_ADDRESS --port $LISTEN_PORT --tls-key $TLS_KEY_PATH --tls-crt $TLS_CERT_PATH
