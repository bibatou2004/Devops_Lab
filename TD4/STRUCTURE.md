# 📁 Project Structure - TD4

## Complete File Hierarchy

```
TD4/
│
├── README.md                              # Main documentation
├── STRUCTURE.md                           # This file
├── TESTING_BEST_PRACTICES.md             # Testing guide
│
├── devops-lab/                            # Git repository
│   ├── .git/                              # Git configuration
│   ├── .gitignore
│   ├── README.md                          # Course overview
│   ├── TD1/                               # Module 1
│   ├── TD2/                               # Module 2
│   ├── TD3/                               # Module 3
│   └── TD4/                               # Module 4 (This project)
│
└── scripts/
    │
    ├── sample-app/                        # Node.js Application
    │   ├── app.js                         # Express app (exports)
    │   ├── server.js                      # Server entry point
    │   ├── package.json                   # NPM configuration
    │   ├── package-lock.json              # Dependency lock file
    │   ├── jest.config.js                 # Jest configuration
    │   ├── Dockerfile                     # Docker image definition
    │   ├── build-docker-image.sh          # Build script
    │   ├── docker_image_id.txt            # Generated Docker ID
    │   ├── deployment_template.tpl        # Deployment template
    │   ├── README.md                      # App documentation
    │   ├── TESTING_BEST_PRACTICES.md     # Testing guide
    │   │
    │   ├── node_modules/                  # Dependencies (generated)
    │   │   ├── express/
    │   │   ├── jest/
    │   │   └── supertest/
    │   │
    │   ├── coverage/                      # Test coverage (generated)
    │   │   ├── lcov-report/
    │   │   ├── coverage-final.json
    │   │   └── ...
    │   │
    │   ├── __tests__/                     # Test files
    │   │   ├── unit/
    │   │   │   ├── app.test.js            # Unit tests
    │   │   │   └── tdd-example.test.js    # TDD example
    │   │   └── integration/
    │   │       └── app.integration.test.js # Integration tests
    │   │
    │   ├── src/                           # Source code
    │   │   └── index.js                   # Lambda handler
    │   │
    │   └── lambda_function.zip            # Packaged Lambda (generated)
    │
    └── tofu/                              # Terraform Infrastructure
        │
        ├── modules/                       # Reusable modules
        │   └── test-endpoint/             # Test endpoint module
        │       ├── main.tf                # Module resources
        │       ├── variables.tf           # Module variables
        │       └── outputs.tf             # Module outputs
        │
        └── live/                          # Live configurations
            └── lambda-sample/             # Lambda sample project
                ├── main.tf                # Main configuration
                ├── variables.tf           # Removed (merged into main.tf)
                ├── outputs.tf             # Removed (merged into main.tf)
                │
                ├── deploy.tftest.hcl      # Deployment tests
                ├── error-test.tftest.hcl  # Error scenario tests
                ├── test-local.tftest.hcl  # Local tests
                ├── test.sh                # Automated test script
                │
                ├── deployment_template.tpl # Deployment result template
                ├── README.md              # Terraform documentation
                │
                ├── .terraform/            # Generated (Terraform working dir)
                ├── .terraform.lock.hcl    # Provider lock file
                ├── terraform.tfstate      # State file (generated)
                ├── terraform.tfstate.backup
                ├── tfplan                 # Plan file (generated)
                │
                ├── lambda_config.json     # Generated Lambda config
                ├── api_config.json        # Generated API config
                └── deployment_result.txt  # Generated deployment summary
```

---

## 📊 File Statistics

### By Type

| Type | Count |
|------|-------|
| JavaScript Files | 4 |
| Test Files | 3 |
| Terraform Files | 5 |
| Configuration Files | 8 |
| Documentation | 6 |
| Shell Scripts | 2 |

### By Size Category

| Category | Size | Files |
|----------|------|-------|
| Large (>1MB) | node_modules/ | Generated |
| Medium (10KB-1MB) | coverage/ | Generated |
| Small (<10KB) | Source code | ~15 |
| Generated | Various | Multiple |

---

## 🔄 Workflow

### Development Flow

```
Code Changes
    ↓
Unit Tests (Jest)
    ↓
Integration Tests
    ↓
Code Coverage Check
    ↓
Infrastructure Tests (Terraform)
    ↓
Git Commit
    ↓
GitHub Push
    ↓
✅ Complete
```

### Testing Flow

```
npm test
    ├── Jest Configuration
    ├── Unit Tests (__tests__/unit/)
    ├── Integration Tests (__tests__/integration/)
    └── Coverage Report (coverage/)

./test.sh (Terraform)
    ├── Format Check
    ├── Syntax Validation
    ├── Plan Creation
    ├── Apply Configuration
    ├── Output Verification
    ├── File Verification
    └── Cleanup
```

---

## 📝 Key Files

### Application Code

- **app.js**: Core Express application (exports app)
- **server.js**: Server initialization (requires app)
- **package.json**: Project metadata and dependencies

### Testing

- **jest.config.js**: Jest configuration
- **__tests__/unit/app.test.js**: Unit tests
- **__tests__/integration/app.integration.test.js**: Integration tests

### Infrastructure

- **scripts/tofu/live/lambda-sample/main.tf**: Terraform main config
- **scripts/tofu/live/lambda-sample/test.sh**: Automated tests
- **scripts/tofu/live/lambda-sample/deployment_template.tpl**: Template

### Documentation

- **README.md**: Main project guide
- **STRUCTURE.md**: This file
- **TESTING_BEST_PRACTICES.md**: Testing guidelines

---

## 🎯 Quick Navigation

| What | Where |
|------|-------|
| Start application | `scripts/sample-app/` → `npm start` |
| Run tests | `scripts/sample-app/` → `npm test` |
| Build Docker | `scripts/sample-app/` → `./build-docker-image.sh` |
| Deploy infrastructure | `scripts/tofu/live/lambda-sample/` → `./test.sh` |
| View coverage | `scripts/sample-app/coverage/lcov-report/index.html` |

---

## 🔐 Git Configuration

```
Repository: devops-lab/
Main Branch: main
Remote: https://github.com/bibatou2004/Devops_Lab.git
```

---

## 📦 Dependencies

### Production

- express (v4.18+)

### Development

- jest (v29+)
- supertest (v6+)

### Infrastructure

- terraform (v1.0+)
- hashicorp/local provider

---

## Generated Files (Ignored in Git)

```
node_modules/              # NPM dependencies
coverage/                  # Test coverage reports
.terraform/                # Terraform working directory
terraform.tfstate*         # Terraform state files
*.zip                      # Lambda packages
tfplan                     # Terraform plans
```

