# Testing Best Practices - DevOps Lab

## 1. The Test Pyramid 🔺

```
        /\
       /E2E\        End-to-End Tests (10%)
      /      \      - Full application flow
     /Integration\  Integration Tests (20%)
    /            \ - Component integration
   /Unit Tests   \ Unit Tests (70%)
  /________________ - Fast isolated tests
```

### Unit Tests (70% of efforts)
- **Speed**: Milliseconds
- **Scope**: Single function/component
- **Isolation**: No external dependencies
- **Example**: Testing `/add/:a/:b` endpoint

### Integration Tests (20% of efforts)
- **Speed**: Seconds
- **Scope**: Multiple components
- **Example**: User workflow (login → add item → logout)

### End-to-End Tests (10% of efforts)
- **Speed**: Minutes
- **Scope**: Full application
- **Example**: Complete user journey in production-like environment

---

## 2. What to Test ✅

### Critical Path
- Authentication & Authorization
- Payment/Transaction processing
- Data consistency

### Edge Cases
- Empty/null inputs
- Very large inputs
- Special characters
- Boundary values

### Error Scenarios
- Invalid input validation
- Network failures
- Database errors
- HTTP error codes (400, 404, 500)

---

## 3. Test-Driven Development (TDD) 🔄

### Cycle: Red → Green → Refactor

**Step 1: RED** - Write failing test
```javascript
test('GET /api/users/:id returns user', async () => {
  const res = await request(app).get('/api/users/1');
  expect(res.statusCode).toBe(200);
  expect(res.body.id).toBe(1);
});
```

**Step 2: GREEN** - Write minimal code to pass
```javascript
app.get('/api/users/:id', (req, res) => {
  res.json({ id: parseInt(req.params.id) });
});
```

**Step 3: REFACTOR** - Improve without breaking tests
```javascript
app.get('/api/users/:id', (req, res) => {
  const user = getUserFromDB(req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json(user);
});
```

---

## 4. Code Coverage 📊

### Metrics

| Metric | Target | Tool |
|--------|--------|------|
| Line Coverage | > 80% | Jest --coverage |
| Branch Coverage | > 70% | Jest --coverage |
| Function Coverage | > 80% | Jest --coverage |

### Important Note
- 100% coverage ≠ Bug-free code
- Focus on critical paths first
- Quality > Quantity

### Generating Coverage Report
```bash
npm test -- --coverage
open coverage/lcov-report/index.html
```

---

## 5. Testing in CI/CD Pipeline 🚀

### Recommended Pipeline

```yaml
stages:
  - Lint & Format
    - eslint .
    - prettier --check .
    
  - Unit Tests
    - npm test
    - Coverage > 80%
    
  - Integration Tests
    - npm run test:integration
    - docker-compose tests
    
  - Security Scan
    - npm audit
    - trivy scan docker_image
    
  - Infrastructure Tests
    - terraform validate
    - tfsec scan
    
  - Deploy to Staging
    - Build docker image
    - Deploy to staging
    - Run E2E tests
    
  - Deploy to Production
    - Manual approval
    - Deploy to production
    - Monitor health
```

---

## 6. Terraform/Infrastructure Testing 🏗️

### Validation Steps

```bash
# 1. Format check
terraform fmt -check .

# 2. Syntax validation
terraform validate

# 3. Security scan
tfsec .
checkov -d .

# 4. Plan review
terraform plan

# 5. Automated tests
terraform test
```

---

## 7. Docker Image Testing 🐳

```bash
# Build image
docker build -t myapp:v1 .

# Scan for vulnerabilities
trivy image myapp:v1

# Run container
docker run -d --name test myapp:v1

# Test application
curl http://localhost:8080/

# Check logs
docker logs test

# Cleanup
docker stop test
docker rm test
```

---

## 8. Checklist Before Deployment ✔️

- [ ] All tests passing
- [ ] Code coverage > 80%
- [ ] No security vulnerabilities
- [ ] Code review approved
- [ ] Documentation updated
- [ ] Performance acceptable
- [ ] Rollback plan documented
- [ ] Monitoring configured

---

## 9. Metrics & KPIs 📈

Track these metrics to improve testing:
- Test coverage percentage
- Bug detection rate
- Time to fix bugs
- Test execution time
- False positive rate

---

## Resources

- [Jest Documentation](https://jestjs.io/)
- [Testing Library](https://testing-library.com/)
- [Terraform Testing](https://www.terraform.io/language/tests)
- [Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html)

