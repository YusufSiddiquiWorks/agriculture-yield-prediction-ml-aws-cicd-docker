FROM python:3.11-slim

WORKDIR /app

COPY dockerrequirements.txt .

COPY . .

RUN python -m pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r dockerrequirements.txt

EXPOSE 7002

ENTRYPOINT [ "python3", "app.py" ]