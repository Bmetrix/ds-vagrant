# Minimal Dockerfile that runs a Python broadcast-based script
FROM python:3.9-slim

# Nastavení nebufferovaného výstupu pro Python
ENV PYTHONUNBUFFERED=1

COPY python/color-broadcast.py /opt/color-broadcast.py
RUN chmod +x /opt/color-broadcast.py

# By default, run the color-broadcast script
CMD ["python", "/opt/color-broadcast.py"]
