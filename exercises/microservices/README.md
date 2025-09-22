# Lab 4: Event-Driven Microservices Architecture

## Objective
Use Codex to build a complete microservices system with multiple languages, message queues, and Docker orchestration.

## System Overview

Build an e-commerce order processing system with:

1. **Auth Service** (Node.js/Express)
   - JWT authentication
   - User management
   - Role-based access control

2. **Order Service** (Python/FastAPI)
   - Order creation and management
   - Inventory checking
   - Payment processing integration

3. **Notification Service** (Go)
   - Email notifications
   - SMS alerts
   - Push notifications

4. **Analytics Service** (Java/Spring Boot)
   - Real-time metrics
   - Order analytics
   - Revenue reporting

## Architecture Components

### Message Queue
- RabbitMQ for event-driven communication
- Event sourcing pattern
- CQRS implementation

### Database Strategy
- Auth Service: PostgreSQL
- Order Service: PostgreSQL
- Notification Service: Redis
- Analytics Service: MongoDB

### API Gateway
- Kong or nginx
- Rate limiting
- Request routing
- Authentication

## Codex Prompts Progression

### Step 1: Project Structure
```bash
codex "Create a microservices project structure with docker-compose,
       including services for auth (Node.js), orders (Python),
       notifications (Go), and analytics (Java Spring Boot)"
```

### Step 2: Auth Service
```bash
codex "Build Node.js auth service with Express, JWT, PostgreSQL,
       user CRUD operations, login/logout, and refresh tokens"
```

### Step 3: Order Service
```bash
codex "Create Python FastAPI order service with async handlers,
       PostgreSQL models, Pydantic schemas, and RabbitMQ integration"
```

### Step 4: Notification Service
```bash
codex "Implement Go notification service with RabbitMQ consumer,
       email/SMS providers, template engine, and Redis caching"
```

### Step 5: Analytics Service
```bash
codex "Build Spring Boot analytics service with MongoDB,
       real-time metrics collection, REST API, and WebSocket updates"
```

### Step 6: Message Queue Setup
```bash
codex "Configure RabbitMQ with exchanges, queues, and bindings
       for order events, user events, and notification events"
```

### Step 7: Docker Configuration
```bash
codex "Create Docker configurations for all services with
       multi-stage builds, health checks, and docker-compose orchestration"
```

### Step 8: API Gateway
```bash
codex "Setup nginx API gateway with routing rules, rate limiting,
       JWT validation, and load balancing"
```

### Step 9: Integration Tests
```bash
codex "Create integration tests for the complete workflow:
       user registration -> login -> create order -> receive notification"
```

### Step 10: Monitoring & Logging
```bash
codex "Add Prometheus metrics, Grafana dashboards, and
       centralized logging with ELK stack"
```

## Events & Messages

### Event Types
```json
{
  "UserRegistered": {
    "userId": "uuid",
    "email": "string",
    "timestamp": "ISO8601"
  },
  "OrderCreated": {
    "orderId": "uuid",
    "userId": "uuid",
    "items": [],
    "total": "number"
  },
  "PaymentProcessed": {
    "orderId": "uuid",
    "status": "success|failed",
    "amount": "number"
  },
  "NotificationSent": {
    "type": "email|sms|push",
    "recipient": "string",
    "status": "sent|failed"
  }
}
```

## Service Specifications

### Auth Service (Node.js)
```javascript
// Endpoints
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/refresh
POST   /api/auth/logout
GET    /api/users/profile
PUT    /api/users/profile
DELETE /api/users/:id

// Technologies
- Express.js
- TypeScript
- Prisma ORM
- jsonwebtoken
- bcrypt
- PostgreSQL
```

### Order Service (Python)
```python
# Endpoints
POST   /api/orders
GET    /api/orders
GET    /api/orders/{id}
PUT    /api/orders/{id}/status
DELETE /api/orders/{id}
POST   /api/orders/{id}/payment

# Technologies
- FastAPI
- SQLAlchemy
- Pydantic
- aio-pika (RabbitMQ)
- PostgreSQL
```

### Notification Service (Go)
```go
// Message Handlers
- HandleUserRegistered
- HandleOrderCreated
- HandlePaymentProcessed
- HandleOrderShipped

// Technologies
- Gin framework
- AMQP client
- Redis client
- SendGrid/Twilio
- Template engine
```

### Analytics Service (Java)
```java
// Endpoints
GET  /api/analytics/orders/daily
GET  /api/analytics/revenue/monthly
GET  /api/analytics/users/growth
WS   /api/analytics/realtime

// Technologies
- Spring Boot
- Spring Data MongoDB
- Spring AMQP
- WebSocket
- Micrometer
```

## Docker Compose Configuration

```yaml
version: '3.8'
services:
  auth-service:
    build: ./auth-service
    environment:
      - DATABASE_URL=postgresql://...
      - JWT_SECRET=...
      - RABBITMQ_URL=...

  order-service:
    build: ./order-service
    environment:
      - DATABASE_URL=postgresql://...
      - RABBITMQ_URL=...

  notification-service:
    build: ./notification-service
    environment:
      - REDIS_URL=...
      - RABBITMQ_URL=...

  analytics-service:
    build: ./analytics-service
    environment:
      - MONGODB_URL=...
      - RABBITMQ_URL=...

  rabbitmq:
    image: rabbitmq:3-management

  postgres:
    image: postgres:15

  mongodb:
    image: mongo:6

  redis:
    image: redis:7

  nginx:
    build: ./nginx
    ports:
      - "80:80"
```

## Success Criteria

- [ ] All services running in Docker
- [ ] Services communicate via RabbitMQ
- [ ] API Gateway routing works
- [ ] Authentication flows correctly
- [ ] Orders trigger notifications
- [ ] Analytics updates in real-time
- [ ] Integration tests pass
- [ ] Monitoring dashboard works

## Advanced Challenges

1. Implement saga pattern for distributed transactions
2. Add circuit breakers for resilience
3. Implement distributed tracing with Jaeger
4. Add service mesh with Istio
5. Deploy to Kubernetes

## Testing the System

```bash
# Start all services
docker-compose up -d

# Run integration tests
./scripts/integration-tests.sh

# Check service health
curl http://localhost/health

# Create a user
curl -X POST http://localhost/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Create an order
curl -X POST http://localhost/api/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"productId":"123","quantity":2}]}'

# Check analytics
curl http://localhost/api/analytics/orders/daily

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Monitoring URLs

- RabbitMQ Management: http://localhost:15672
- Grafana Dashboard: http://localhost:3000
- Prometheus: http://localhost:9090
- Application: http://localhost