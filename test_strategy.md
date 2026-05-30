## Test Strategy ## 

**Audio Processing Pipeline — FastAPI + RabbitMQ + Postgres**  
This project implements a modular, message‑driven audio processing pipeline using:
- FastAPI
- RabbitMQ
- Postgres
- AlgoA (Feature Extraction)
- AlgoB (Feature Enrichment / Classification)
- Structured Logging (ELK)
- Allure Reporting
- Pytest
- Locust
  
The system is designed for clarity, testability, and scalability.

## Architecture Overview ##
Sensor → audio_queue → AlgoA → features_a_queue → AlgoB → features_b_queue → DataWriter → Postgres → REST API

## Components ##
- AlgoA — transforms raw audio into FeatureA
- AlgoB — transforms FeatureA into FeatureB
- DataWriter — writes processed features into Postgres
- FastAPI — exposes realtime & historical endpoints
- RabbitMQ — message broker between processing stages
- Postgres — persistent storage

## Message Queue Abstraction Strategy ##
The project uses two separate RabbitMQ clients, each with a clear purpose:

1. <ins>**RabbitMQClient (Production Client)**</ins>  
Located in src/rabbitmq_client.py.
Used by the running application.  

- Connects to a real RabbitMQ broker
- Publishes and consumes real messages
- Handles credentials, vhosts, and network behavior
- Used by API handlers and background workers
- This client is optimized for reliability and production correctness.

2. <ins>**RabbitMQTestClient (In‑Memory Test Client)**</ins>   
Defined inside tests/conftest.py.
Used only during testing.

- Stores messages in memory (Python list)
- No network, no broker, no credentials
- Fully deterministic
- Instant publish/consume
- Safe for CI/CD
- Allows pipeline simulation without real workers
- This client is optimized for speed, isolation, and test determinism.

## A layered QA strategy ##
This project implements a layered QA strategy covering every part of the pipeline.

- **Unit Tests** 
  - Algo A — signal preprocessing, transformations, threshold logic
  - Algo B — classification, scoring, enrichment
  - DataWriter — data formatting, validation, DB write logic 
  - REST API handlers — request validation, response formatting, error handling

- **Integration Tests:**
  
  Sensor → RabbitMQ → Algo A → Algo B → DataWriter → Postgres → API
  
  - Message publishing to RabbitMQ
  - Message consumption by Algo A & Algo B
  - Correct transformation between stages
  - DataWriter writes correct records to Postgres
  - API retrieves correct data from DB

- **API / E2E Tests**
  - Validate full system behavior
  - Ensure correct API contracts
  - Confirm DB + processing + API integration
  - End‑to‑end data flow

- **Performance Tests** 
  - RabbitMQ throughput
  - Algo A & Algo B processing latency
  - API response times
  - Database write/read performance  

- **Security Tests**
  - Authentication & authorization
  - rate limiting
  - injection
  - Payload validation
  - Endpoint hardening

- **Reporting**
  All test results are aggregated using Allure Reports

- **CI/CD Integration with Jenkins**

