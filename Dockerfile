FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src ./src
COPY streamlit_app ./streamlit_app
COPY scripts ./scripts
COPY api ./api
COPY app.py cli.py ./

# Without data/raw/ the app runs on seeded sample data. To show real prices,
# run `python cli.py fetch-data` at startup or mount a volume on /app/data.
EXPOSE 8501
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
