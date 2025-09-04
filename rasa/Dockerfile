# Use official Rasa image as base
FROM rasa/rasa:3.6.13-full

# Set working directory
WORKDIR /app

# Switch to root for installations
USER root

# Install additional dependencies with CPU-only versions
RUN pip install --no-cache-dir \
    spacy==3.7.2 \
    transformers==4.35.2 \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.1.1

# Download spaCy model
RUN python -m spacy download en_core_web_md

# Copy Rasa configuration files
COPY config.yml domain.yml ./
COPY data/ ./data/

# Create models directory
RUN mkdir -p models

# Set permissions
RUN chown -R 1001:1001 /app

# Switch back to rasa user
USER 1001

# Train the model
RUN rasa train --config config.yml --domain domain.yml --data data/ --out models/

# Expose ports
EXPOSE 5005

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:5005/status || exit 1

# Run Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--host", "0.0.0.0", "--port", "5005"] 