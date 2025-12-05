# 🎯 TD4 - Quick Navigation & Overview

## 🚀 Start Here

This is **TD4: Version Control, Build Systems & Testing** - the comprehensive DevOps module.

### What You'll Learn

- Git and GitHub for version control
- NPM for build systems
- Automated testing with Jest
- Infrastructure testing with Terraform
- DevOps best practices

---

## 📂 Quick Navigation

### Application Code
👉 [scripts/sample-app/](scripts/sample-app/)
- **README.md** - Application guide
- **app.js** - Express application
- **__tests__/** - Test files

### Infrastructure
👉 [scripts/tofu/live/lambda-sample/](scripts/tofu/live/lambda-sample/)
- **README.md** - Terraform guide
- **main.tf** - Configuration
- **test.sh** - Automated tests

### Documentation
👉 [README.md](README.md) - Main guide (START HERE!)
👉 [STRUCTURE.md](STRUCTURE.md) - Project structure

---

## ▶️ Getting Started

### 1. Install Dependencies

```bash
cd scripts/sample-app
npm install
```

### 2. Start the Application

```bash
npm start
# Server runs on http://localhost:8080
```

### 3. Test the Endpoints

```bash
# In another terminal:
curl http://localhost:8080/
curl http://localhost:8080/name/Alice
curl http://localhost:8080/add/5/3
```

### 4. Run Tests

```bash
npm test
npm test -- --coverage
```

### 5. Test Infrastructure

```bash
cd ../tofu/live/lambda-sample
./test.sh
```

---

## 📊 Key Files

| File | Purpose | Location |
|------|---------|----------|
| app.js | Express application | scripts/sample-app/ |
| jest.config.js | Test configuration | scripts/sample-app/ |
| main.tf | Terraform config | scripts/tofu/live/lambda-sample/ |
| package.json | Dependencies | scripts/sample-app/ |
| __tests__/unit/ | Unit tests | scripts/sample-app/ |
| __tests__/integration/ | Integration tests | scripts/sample-app/ |

---

## 🧪 Tests

### Unit Tests
```bash
cd scripts/sample-app
npm test -- __tests__/unit/
```

### Integration Tests
```bash
npm test -- __tests__/integration/
```

### Coverage Report
```bash
npm test -- --coverage
open coverage/lcov-report/index.html
```

---

## 🏗️ Infrastructure

### Validate Terraform
```bash
cd scripts/tofu/live/lambda-sample
terraform validate
```

### Run Infrastructure Tests
```bash
./test.sh
```

### Generate Configuration
```bash
terraform plan
terraform apply
```

---

## 📈 Project Stats

```
✅ 5+ Test Files
✅ 30+ Test Cases
✅ 85%+ Code Coverage
✅ 10+ Terraform Files
✅ 2000+ Lines of Code
```

---

## 🎯 Exercises

All 14 exercises completed:

```
✅ Exercise 1-8: Foundations
✅ Exercise 9: Add Endpoint
✅ Exercise 10: Code Coverage
✅ Exercise 11: JSON Responses
✅ Exercise 12: Error Handling
✅ Exercise 13: TDD
✅ Exercise 14: Coverage Analysis
```

---

## 📚 Learn More

- [Main README](README.md)
- [Project Structure](STRUCTURE.md)
- [Testing Best Practices](scripts/sample-app/TESTING_BEST_PRACTICES.md)
- [Application Guide](scripts/sample-app/README.md)
- [Terraform Guide](scripts/tofu/live/lambda-sample/README.md)

---

## 🔗 Useful Commands

```bash
# Navigate to app
cd scripts/sample-app

# Install & Start
npm install && npm start

# Test
npm test

# Coverage
npm test -- --coverage

# Navigate to infrastructure
cd ../tofu/live/lambda-sample

# Test infrastructure
./test.sh

# Terraform commands
terraform init
terraform validate
terraform plan
```

---

## 💡 Tips

- Read [README.md](README.md) first for complete overview
- Check [STRUCTURE.md](STRUCTURE.md) for file organization
- Use npm scripts defined in package.json
- Run tests before each commit
- Keep coverage > 80%

---

## ✅ Success Criteria

- [ ] Application starts on port 8080
- [ ] All endpoints respond correctly
- [ ] All tests pass
- [ ] Coverage > 80%
- [ ] Terraform validates successfully
- [ ] Infrastructure tests pass

---

**Ready to start? Go to [README.md](README.md)!** 🚀

