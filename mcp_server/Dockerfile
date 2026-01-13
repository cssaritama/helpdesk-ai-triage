FROM python:3.11-slim

WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir -e .

COPY mcp /app/mcp

EXPOSE 8765
CMD ["uvicorn", "mcp.server:app", "--host", "0.0.0.0", "--port", "8765"]
