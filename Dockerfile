FROM python:3.11-slim
WORKDIR /app
COPY . .
CMD ["python","-m","flexible_factory.cli","data/example.json"]
