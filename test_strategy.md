## Test Strategy ## 

This project implements a layered QA strategy covering every part of the pipeline.

Test Layers
- Unit Tests — Algo logic, DataWriter, API handlers

- Integration Tests — Sensor → RabbitMQ → Algo A → Algo B → DataWriter → Postgres → API

- API / E2E Tests — Real‑time & historical endpoints

- Performance Tests — Locust

- Security Tests — Auth, rate limiting, injection

All results are aggregated using Allure Reports.
