# TD5 Sample Lambda Application

Application Lambda Python pour AWS API Gateway.

## 📁 Structure

```
sample-app/
├── src/
│   └── app.py           # Application Lambda
├── tests/
│   └── test_app.py      # Tests unitaires
├── config/
│   └── lambda_config.json # Configuration
└── README.md
```

## 🚀 Endpoints

- `GET /` - Health check
- `GET /health` - Health status
- `GET /info` - Application info

## 🧪 Tests

```bash
pytest tests/ -v
```

## 📦 Déploiement

Les workflows GitHub Actions déploient automatiquement:
1. Tests unitaires
2. Terraform plan
3. Terraform apply

