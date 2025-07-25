FROM python:3.13-slim AS builder
 
RUN mkdir /app
 
WORKDIR /app
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
RUN pip install --upgrade pip 
COPY requirements.txt /app/ 
RUN pip install --no-cache-dir -r requirements.txt
 
FROM python:3.13-slim
 
RUN mkdir /app 
 
# Copies the installed Python libraries
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
# Copies executable scripts
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
WORKDIR /app
 
COPY . .
 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
EXPOSE 8000 

RUN chmod +x  /app/entrypoint.prod.sh

CMD ["/app/entrypoint.prod.sh"]