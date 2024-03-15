FROM python:3.11

# Install build dependencies
RUN apt-get update
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    wget \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python packages
RUN pip install --upgrade pip
RUN pip install openai langchain open-interpreter google-search-results anthropic torch chromadb requests llama-index tavily-python

# Clone the gpt-researcher project
RUN git clone https://github.com/assafelovic/gpt-researcher.git
ENV PYTHONPATH="/gpt-researcher:${PYTHONPATH}"

# Change directory to /gpt-researcher, install dependencies, then return to a specified workdir
WORKDIR /gpt-researcher
RUN pip install -r requirements.txt

# Return to the root directory or specify another work directory
WORKDIR /