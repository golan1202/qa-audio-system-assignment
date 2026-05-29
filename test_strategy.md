## Test Strategy ## 

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
  - Validate real‑world usage scenarios

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

- All results are aggregated using **Allure Reports**.

- **CI/CD Integration with Jenkins**
