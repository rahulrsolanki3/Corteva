# Code Challenge Template
# Weather Data ETL & API (SQLite + Flask)

This project implements a small end-to-end pipeline for working with historical weather data:

1. **Ingest** raw daily weather observations (Problem 1 & 2)
2. **Compute yearly statistics** per station (Problem 3)
3. **Expose a REST API** to query raw data and yearly stats (Problem 4, using Flask)

The project uses:

- **SQLite** as the database
- **Python** for ETL and analysis
- **Flask + flasgger** for the REST API and Swagger UI

---
## Problem 5
If this project needed to run in the cloud, I would use AWS services that are managed, reliable, and easy to maintain.
1. Database – Amazon RDS
Instead of SQLite, the database would be moved to Amazon RDS PostgreSQL.
RDS handles backups, scaling, and availability automatically.
Credentials would be stored securely in AWS Secrets Manager.
2. API Deployment – Flask on ECS Fargate
The Flask API would be packaged into a Docker container and deployed on Amazon ECS Fargate, which runs containers without needing servers.
The container image would be stored in Amazon ECR, and an Application Load Balancer would route traffic to the API.
3. Scheduled Data Ingestion – EventBridge + ECS Task
The ingestion script (answers/cli.py) would run on a schedule using Amazon EventBridge (cron-like scheduler).
EventBridge would trigger a small ECS Fargate task that runs:
python -m answers.cli
Raw weather data files would be stored in Amazon S3, and the ingestion code would read from S3 instead of local disk.
4. Infrastructure as Code
The entire setup (API, database, scheduler, networking) would be defined using Terraform or CloudFormation, making deployment repeatable and easy for others to set up.

## Project Structure

```text
.
├─ wx_data/                  # Raw weather data files (.txt) go here
├─ answers/
│  ├─ __init__.py
│  ├─ config.py              # Paths for DB + data directory
│  ├─ db.py                  # DB connection + table creation
│  ├─ ingest.py              # Ingestion of raw .txt files into SQLite
│  ├─ stats.py               # Yearly statistics computation
│  ├─ cli.py                 # ETL pipeline entrypoint (Problems 1–3)
│  └─ api.py                 # Flask API (Problem 4)
├─ weather.db                # SQLite DB (created after first ETL run)

Run the following steps:
1. python -m answers.cli / python3 -m answers.cli
2. python -m answers.api
Flask runs on http://localhost:5000

