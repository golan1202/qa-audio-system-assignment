# Test design for audio processing system

## 1. Types of tests

### 1.1 Unit tests

**Scope:**

- Sensor message formatting (where simulated)
- Algorithm A processing logic
- Algorithm B processing logic
- DataWriter transformation and validation logic
- REST API handlers (validation, serialization, error handling)

**What is being tested?**

- Correct handling of JSON input and output schemas
- Deterministic feature extraction in Algo A and Algo B
- Correct enrichment and normalization of feature records in DataWriter
- REST API request/response behavior (status codes, payload structure, error responses)

**Why is it important?**

- Catches logic bugs early and cheaply
- Ensures algorithms are stable and reproducible
- Provides fast feedback in CI/CD
- Makes refactoring safe

**Expected outcomes:**

- Given valid audio JSON → Algo A returns valid Feature A JSON with required fields
- Given valid Feature A JSON → Algo B returns valid Feature B JSON with required fields
- DataWriter accepts valid feature messages and rejects malformed ones with clear errors
- REST API returns correct HTTP codes, JSON schema, and error messages for edge cases

---

### 1.2 Integration tests

**Scope:**

- Sensors → RabbitMQ (message format, routing keys, queues)
- RabbitMQ → Algo A pods (load‑balanced consumption)
- Algo A → Features Stream → Algo B
- Features Stream → DataWriter → DB
- REST API → DB (historical) and Features queue (real‑time)

**What is being tested?**

- End‑to‑end message flow between components
- Correct queue bindings and routing
- Idempotency and at‑least‑once processing behavior
- Data consistency between features in queues and DB
- Real‑time vs historical paths in REST API

**Why is it important?**

- Validates that independently correct components actually work together
- Surfaces configuration issues (queues, env vars, connection strings)
- Ensures no data loss or duplication in the pipeline
- Confirms that external clients see coherent data

**Expected outcomes:**

- A synthetic audio message published to the audio queue eventually produces Feature A and Feature B messages in the features queue
- DataWriter writes all features to DB with correct timestamps and sensor IDs
- REST API returns the same data via real‑time and historical paths for overlapping time windows
- No messages are stuck in queues under normal operation

---

### 1.3 Load & performance tests

**Scope:**

- RabbitMQ throughput under high sensor load
- Algo A and Algo B pod scaling behavior
- DataWriter throughput and DB write latency
- REST API latency and error rate under concurrent clients

**What is being tested?**

- System behavior under realistic and peak loads
- Queue depth, processing latency, and back‑pressure
- Horizontal scaling of Kubernetes pods
- REST API response times and saturation point

**Why is it important?**

- Ensures the system can handle production traffic safely
- Identifies bottlenecks (CPU, IO, DB, queues)
- Provides capacity planning data
- Prevents cascading failures under load

**Expected outcomes:**

- Defined SLAs (e.g., p95 REST API latency < 300 ms for real‑time, < 500 ms for historical)
- Maximum sustainable messages/sec from sensors without backlog growth
- Stable CPU/memory usage for Algo pods under load
- No DB timeouts or excessive connection pool exhaustion

---

### 1.4 Security tests

**Scope:**

- REST API authentication and authorization
- Input validation and injection protection
- Transport security (HTTPS, TLS)
- Rate limiting and brute‑force protection

**What is being tested?**

- Only authorized clients can access REST API endpoints
- Malicious payloads (SQL injection, JSON injection, path traversal) are rejected
- Sensitive data is not leaked in responses or logs
- Rate limits and throttling are enforced

**Why is it important?**

- System is exposed to the internet
- Protects data integrity and confidentiality
- Reduces attack surface and compliance risk

**Expected outcomes:**

- Unauthorized requests receive 401/403
- Invalid or malicious payloads receive 400 with safe error messages
- All external access uses HTTPS
- Rate limits trigger 429 responses when exceeded

---

### 1.5 Manual vs automated tests

**Automated:**

- All unit tests (Pytest)
- Most integration tests (Pytest + Docker/K8s test environment)
- REST API functional tests (Pytest + requests / Postman collections in CI)
- Load tests (Locust/JMeter) as part of scheduled or pre‑release pipeline
- Basic security checks (dependency scanning, static analysis, basic auth tests)

**Manual:**

- Exploratory testing of REST API and UI (if any)
- Chaos / failure injection scenarios (e.g., killing pods, DB down) initially
- Usability and observability validation (logs, dashboards)
- One‑off deep security assessments (e.g., with specialized tools)

---

## 2. Coverage

### 2.1 Sensors → RabbitMQ

- **Tests:**
  - Validate JSON schema of sensor messages
  - Validate routing key and queue name configuration
  - Validate retry behavior on connection failure (if implemented)
- **Approach:**
  - Simulate sensors with Python scripts publishing to RabbitMQ
  - Use integration tests to assert messages arrive in the correct queue

### 2.2 Algorithm A & B pods

- **Tests:**
  - Unit tests for pure processing logic
  - Integration tests consuming from and publishing to RabbitMQ
  - Load tests to measure processing throughput per pod
- **Approach:**
  - Use test queues in RabbitMQ
  - Spin up test instances of Algo A/B (or run locally with test config)
  - Assert that for N input messages, N output messages are produced with correct mapping

### 2.3 DataWriter → DB

- **Tests:**
  - Unit tests for transformation and validation logic
  - Integration tests with a test DB (e.g., PostgreSQL in Docker)
  - Idempotency tests (reprocessing same message)
- **Approach:**
  - Use a dedicated test schema or database
  - Verify that all fields from features messages are persisted correctly
  - Verify behavior on DB errors (retries, dead‑letter queues if applicable)

### 2.4 REST API (real‑time and historical)

- **Tests:**
  - Unit tests for handlers and serializers
  - Integration tests hitting the API with test data in queues and DB
  - Performance tests for concurrent clients
- **Approach:**
  - Use Pytest + requests or Postman collections
  - For real‑time: publish messages to features queue and verify API returns them within X minutes window
  - For historical: insert records into DB and verify correct filtering by time range and sensor ID

### 2.5 External client access

- **Tests:**
  - End‑to‑end tests from “client” perspective (black‑box)
  - Security tests (auth, TLS, rate limiting)
- **Approach:**
  - Use a dedicated test client script or Postman
  - Run from outside the cluster (or simulate via network rules)
  - Validate that only exposed endpoints are reachable and behave as documented

---

## 3. Test objectives per test type

### 3.1 Unit tests

- **Objective:** Validate correctness of individual functions/classes in isolation.
- **Focus:** Business logic, edge cases, error handling.
- **Success criteria:** High coverage on core logic (Algo A/B, DataWriter, API handlers), fast execution (< seconds).

### 3.2 Integration tests

- **Objective:** Validate that components interact correctly via RabbitMQ, DB, and HTTP.
- **Focus:** Message flow, configuration, data consistency.
- **Success criteria:** All critical flows (sensor → features → DB → API) pass reliably in a realistic environment.

### 3.3 Load & performance tests

- **Objective:** Validate system behavior under expected and peak loads.
- **Focus:** Throughput, latency, resource usage, stability.
- **Success criteria:** SLAs met, no uncontrolled backlog growth, no crashes or severe degradation.

### 3.4 Security tests

- **Objective:** Validate that the exposed REST API is secure against common attacks and misconfigurations.
- **Focus:** Auth, input validation, TLS, rate limiting.
- **Success criteria:** No unauthenticated access to protected data, no obvious injection vectors, secure defaults.

### 3.5 Manual tests

- **Objective:** Discover issues not covered by automated tests and validate overall usability and observability.
- **Focus:** Exploratory flows, error scenarios, logs and dashboards.
- **Success criteria:** No critical UX or observability gaps before release.

---

## 4. Automation strategy

### 4.1 What to automate

- **Unit tests:** 100% automated with Pytest.
- **Integration tests:** Automated with Pytest + Docker/K8s test environment.
- **API tests:** Automated with Pytest + requests or Postman collections in CI.
- **Performance tests:** Automated via Locust or JMeter, triggered on demand or pre‑release.
- **Security checks:** Automated dependency scanning (e.g., GitHub Dependabot), basic auth tests in CI.

### 4.2 Tools

- **Python testing:** Pytest
- **API testing:** Pytest + requests, optional Postman collections + Newman
- **Load testing:** Locust (Python‑based) or JMeter
- **Mocking:** unittest.mock / pytest‑mock
- **Containers:** Docker + docker‑compose or K8s test namespace
- **CI/CD:** GitHub Actions (or Jenkins)



## 5. CI/CD Integration

### 5.1 Pipeline Stages

- Code checkout
- Dependency installation
- Static analysis (flake8, black, mypy)
- Unit tests
- Integration tests (RabbitMQ + DB services)
- API tests
- Performance tests (scheduled)
- Security scanning
- Reporting & notifications
- Deploy to staging environment

### 5.2 Tools

- GitHub Actions
- Docker + docker-compose
- Pytest
- Allure / JUnit XML
- Slack / Teams notifications


## 6. Logging & Visualization Tools

### 6.1 Logging

- **ELK / EFK stack**

- **Log fields:**
  - message_id
  - sensor_id
  - timestamps at each stage
  - queue consumption events
  - API request/response metadata

### 6.2 Metrics
- Prometheus
- Grafana dashboards

- **Key metrics:**
  - Queue depth
  - Processing latency
  - API latency
  - Pod CPU/memory