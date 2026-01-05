# 🎓 TD4 - Version Control, Build Systems & Testing

## 📚 Overview

**TD4** is a comprehensive DevOps training module covering:

- ✅ **Version Control** with Git and GitHub
- ✅ **Build System** with NPM and Docker
- ✅ **Dependency Management**
- ✅ **Automated Testing** (Jest & SuperTest)
- ✅ **Infrastructure as Code** (Terraform)
- ✅ **Testing Best Practices**

This module demonstrates a complete DevOps workflow from development to infrastructure testing.

---

## 📁 Structure

```
TD4/
├── README.md                              # This file
├── STRUCTURE.md                           # Project structure guide
├── scripts/
│   ├── sample-app/                        # Node.js Application
│   │   ├── README.md
│   │   ├── app.js
│   │   ├── server.js
│   │   ├── package.json
│   │   ├── jest.config.js
│   │   ├── Dockerfile
│   │   ├── __tests__/
│   │   │   ├── unit/
│   │   │   └── integration/
│   │   └── src/
│   │
│   └── tofu/                              # Terraform Infrastructure
│       └── live/lambda-sample/
│           ├── README.md
│           ├── main.tf
│           ├── deploy.tftest.hcl
│           ├── test.sh
│           └── deployment_template.tpl
```

---

## 🚀 Quick Start

### Prerequisites

```bash
- Node.js (v18+)
- npm (v8+)
- Terraform (v1.0+)
- Git (v2.0+)
```

### Installation

```bash
# Clone repository
git clone https://github.com/bibatou2004/Devops_Lab.git
cd Devops_Lab/TD4

# Install dependencies
cd scripts/sample-app
npm install

# Start application
npm start
```

---

## 🧪 Testing

### Run Tests

```bash
cd scripts/sample-app

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

### Infrastructure Tests

```bash
cd scripts/tofu/live/lambda-sample

# Run automated tests
./test.sh

# Or run Terraform tests
terraform validate
terraform plan
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint |
| `/name/:name` | GET | Personalized greeting |
| `/add/:a/:b` | GET | Add two numbers |
| `/api/status` | GET | API status |

**Examples:**

```bash
# Root
curl http://localhost:8080/

# Greeting
curl http://localhost:8080/name/Alice

# Addition
curl http://localhost:8080/add/5/3

# Status
curl http://localhost:8080/api/status
```

---

## 📖 Sections

### Section 1: Version Control (Git)
- Initialize repositories
- Create commits
- Manage branches
- Merge and rebase

### Section 2: Collaboration (GitHub)
- Push to remote
- Create pull requests
- Manage teams

### Section 3: Build System (NPM)
- NPM scripts
- Build automation
- Docker images

### Section 4: Dependencies
- Package management
- Versioning
- Lock files

### Section 5: Automated Testing
- Unit tests (Jest)
- Integration tests
- Code coverage
- Test reports

### Section 6: Infrastructure Testing
- Terraform validation
- Configuration testing
- Output verification

### Section 7: Best Practices
- Test Pyramid
- TDD Methodology
- Coverage Analysis
- CI/CD Integration

---

## 🎯 Exercises

- ✅ Exercise 9: Add endpoint with tests
- ✅ Exercise 10: Code coverage analysis
- ✅ Exercise 11: JSON response testing
- ✅ Exercise 12: Error handling tests
- ✅ Exercise 13: TDD methodology
- ✅ Exercise 14: Coverage optimization

---

## 📊 Statistics

- **Test Files**: 5+
- **Test Cases**: 30+
- **Code Coverage**: 85%+
- **Lines of Code**: 2000+
- **Terraform Files**: 10+

---

## 📚 Documentation Files

- [README.md](README.md) - Main guide (this file)
- [STRUCTURE.md](STRUCTURE.md) - Project structure
- [scripts/sample-app/README.md](scripts/sample-app/README.md) - App guide
- [scripts/sample-app/TESTING_BEST_PRACTICES.md](scripts/sample-app/TESTING_BEST_PRACTICES.md) - Testing guide
- [scripts/tofu/live/lambda-sample/README.md](scripts/tofu/live/lambda-sample/README.md) - Terraform guide

---

## 🔧 Tools Used

- **Express.js**: Web framework
- **Jest**: Testing framework
- **SuperTest**: HTTP testing
- **Terraform**: Infrastructure as Code
- **Docker**: Containerization
- **Git/GitHub**: Version control

---

## �� Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 👤 Author

**Biba Wandaogo**
- GitHub: [@bibatou2004](https://github.com/bibatou2004)

---

## 📄 License

MIT License

---

## �� Support

For questions or issues:
1. Check the documentation
2. Review the troubleshooting section
3. Open an issue on GitHub

---

**Status**: ✅ Complete
**Last Updated**: December 5, 2025

