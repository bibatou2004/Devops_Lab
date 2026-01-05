# 📱 Sample Node.js Application

A simple Node.js application built with Express.js for the DevOps Lab TD4 course.

## 🚀 Features

- Simple REST API endpoints
- Comprehensive test suite (Jest + SuperTest)
- Docker support
- Terraform configuration
- High code coverage (>85%)

## 📋 Endpoints

| Path | Method | Description |
|------|--------|-------------|
| `/` | GET | Root endpoint |
| `/name/:name` | GET | Personalized greeting |
| `/add/:a/:b` | GET | Add two numbers |
| `/api/status` | GET | API status |

## 🛠️ Installation

```bash
# Install dependencies
npm install

# Start the application
npm start

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

## 📊 API Examples

```bash
# Root endpoint
curl http://localhost:8080/
# Output: Hello, World!

# Personalized greeting
curl http://localhost:8080/name/Alice
# Output: Hello, Alice!

# Add numbers
curl http://localhost:8080/add/5/3
# Output: {"a":5,"b":3,"sum":8}

# API Status
curl http://localhost:8080/api/status
# Output: {"status":"OK","timestamp":"..."}
```

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run specific test file
npm test -- __tests__/unit/app.test.js

# Generate coverage report
npm test -- --coverage
```

## 🐳 Docker

```bash
# Build Docker image
./build-docker-image.sh

# Run Docker container
docker run -p 8080:8080 sample-app:latest
```

## 📁 Project Structure

```
sample-app/
├── app.js                    # Express application
├── server.js                 # Server entry point
├── package.json              # NPM configuration
├── jest.config.js            # Jest configuration
├── Dockerfile                # Docker configuration
├── __tests__/                # Test files
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
└── src/                      # Source code
    └── index.js              # Lambda handler
```

## 📈 Code Coverage

Target coverage: **> 80%**

```bash
npm test -- --coverage
```

## 🔗 Dependencies

- **express**: Web framework
- **jest**: Testing framework
- **supertest**: HTTP testing

## 📄 License

MIT

## 👤 Author

Biba Wandaogo

