FROM python:3.12-slim
WORKDIR /agent
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY sentinel_agent ./sentinel_agent
CMD ["python", "-m", "sentinel_agent.main"]
