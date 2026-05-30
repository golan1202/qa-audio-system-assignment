# QA Automation Assignment – Audio Processing System

This repository contains a complete test design and example implementation for an audio processing system running on Kubernetes with RabbitMQ, algorithms A/B, a DataWriter, and a REST API.

## Repository structure

```text
.
qa-audio-system-assignment/
├─ README.md
├─ design.md
├─ test_strategy.md
├─ conftest.py
├─ pytest.ini
├─ requirements.txt
├─ .gitignore
├─ .env
│
├─ src/
│  ├─ algo_a.py
│  ├─ algo_b.py
│  ├─ data_writer.py
│  ├─ rest_api.py
|  |- rabbitmq_client.py
|  |- consumer.py
│  └─ models.py
│
├─ tests/
│  ├─ unit/
│  │  ├─ test_algo_a.py
│  │  ├─ test_algo_b.py
│  │  ├─ test_data_writer.py
│  │  └─ test_rest_api_unit.py
│  │
│  ├─ integration/
│  │  ├─ test_sensors_to_rabbitmq.py
│  │  ├─ test_algo_a_rabbitmq_flow.py
│  │  ├─ test_algo_b_rabbitmq_flow.py
│  │  ├─ test_datawriter_db_flow.py
│  │  └─ test_rest_api_end_to_end.py
│  │
│  ├─ performance/
│  │  └─ locustfile.py
│  │
│  └─ security/
│     └─ test_rest_api_security.py
```



## Setup Instructions

**Install dependencies**
```text
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Run unit tests**
```text
pytest tests/unit
```
**Run security tests**
```text
pytest tests/security
```
**Run integration tests**
```text
pytest tests/integration
```
**Run REST API**
```text
uvicorn src.rest_api:app --reload --port 8000
```
**Run performance tests**
```text
jmeter -n -t jmeter-plan.jmx -l results.jtl
```
You can then generate an HTML report with:
allure serve reports/allure

### Jenkins CI/CD Setup Prerequisites ###
Jenkins 2.440+  
<ins>Jenkins plugins:</ins>
- Pipeline
- Allure Jenkins Plugin
- Docker Pipeline
- Git
- Docker installed on the Jenkins agent
- Python 3.10+ installed on the Jenkins agent
