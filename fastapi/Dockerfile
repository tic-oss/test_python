# First stage: Building the microservices
FROM python:3.9 AS builder

# Set working directory for both microservices
WORKDIR /app

# Copy and install dependencies for the first microservice
COPY fastapi/posts/requirements.txt /app/service1/
RUN pip install --upgrade pip
RUN pip install -r fastapi/posts/requirements.txt

# Copy source code for the first microservice
COPY fastapi/posts/ /app/service1/

# Copy and install dependencies for the second microservice
COPY fastapi/slack/requirements.txt /app/service2/
RUN pip install -r fastapi/slack/requirements.txt

# Copy source code for the second microservice
COPY fastapi/slack/ /app/service2/

# Final stage: Combining the microservices into one image
FROM python:3.9  

# Copy built microservices from the previous stage
COPY --from=builder /app/service1 /service1
COPY --from=builder /app/service2 /service2

# Set working directory
WORKDIR /service2

# Expose ports for both microservices
EXPOSE 9000
EXPOSE 9001

# Run both microservices sequentially
CMD ["sh", "-c", "uvicorn service1.main:app --host 0.0.0.0 --port 9001 & python service2/main.py"]

