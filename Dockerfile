# Use Node.js as base for Newman
FROM postman/newman:latest

# Copy Postman collection
COPY collection.json /etc/postman/collection.json

# Install Python for email processing
RUN apt-get update && apt-get install -y python3 python3-pip jq
COPY email_sender.py /email_sender.py
RUN pip3 install requests

# Entry point for the container
CMD ["sh", "-c", " \
    while true; do \
        echo 'Authenticating...'; \
        newman run /etc/postman/collection.json \
            --folder Login \
            --reporter-json-export /tmp/login_result.json; \
        echo 'Fetching errors...'; \
        newman run /etc/postman/collection.json \
            --folder GetErrors \
            --reporter-json-export /tmp/errors_result.json; \
        ERROR_JSON=$(cat /tmp/errors_result.json | jq -r '.run.executions[0].response.stream'); \
        python3 /email_sender.py \"$ERROR_JSON\"; \
        sleep 300; \
    done"]
