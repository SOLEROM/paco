FROM ubuntu:22.04

# Non-interactive mode
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl wget gnupg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pull the model at build time (cached into the final image)
RUN ollama pull llama3.2

# Expose Ollama API port
EXPOSE 11434

# Start Ollama server
CMD ["/bin/bash", "-lc", "ollama serve"]

