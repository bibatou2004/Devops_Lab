#!/bin/bash
set -e

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Terraform Testing Suite - DevOps Lab                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test 1: Format Check
echo -e "${BLUE}🔍 Test 1: Format Check${NC}"
if terraform fmt -check -recursive . > /dev/null 2>&1; then
  echo -e "${GREEN}✅ Format OK${NC}"
else
  echo -e "${RED}❌ Format needs correction${NC}"
  echo "Formatting files..."
  terraform fmt -recursive .
  echo -e "${GREEN}✅ Files formatted${NC}"
fi
echo ""

# Test 2: Syntax Validation
echo -e "${BLUE}🔍 Test 2: Syntax Validation${NC}"
if terraform validate > /dev/null 2>&1; then
  echo -e "${GREEN}✅ Validation OK${NC}"
else
  echo -e "${RED}❌ Validation Failed${NC}"
  terraform validate
  exit 1
fi
echo ""

# Test 3: Plan Creation
echo -e "${BLUE}🔍 Test 3: Plan Creation${NC}"
if terraform plan -out=tfplan -no-color > /dev/null 2>&1; then
  echo -e "${GREEN}✅ Plan OK${NC}"
else
  echo -e "${RED}❌ Plan Failed${NC}"
  terraform plan
  exit 1
fi
echo ""

# Test 4: Configuration Apply
echo -e "${BLUE}🔍 Test 4: Configuration Apply${NC}"
if terraform apply -auto-approve tfplan > /dev/null 2>&1; then
  echo -e "${GREEN}✅ Apply OK${NC}"
else
  echo -e "${RED}❌ Apply Failed${NC}"
  terraform apply -auto-approve tfplan
  exit 1
fi
echo ""

# Test 5: Verify Outputs
echo -e "${BLUE}🔍 Test 5: Verify Outputs${NC}"
LAMBDA_ARN=$(terraform output -raw lambda_function_arn 2>/dev/null || echo "")
API_ENDPOINT=$(terraform output -raw api_endpoint 2>/dev/null || echo "")

if [ -z "$LAMBDA_ARN" ] || [ -z "$API_ENDPOINT" ]; then
  echo -e "${RED}❌ Outputs Failed${NC}"
  exit 1
fi

echo "  Lambda ARN: $LAMBDA_ARN"
echo "  API Endpoint: $API_ENDPOINT"
echo -e "${GREEN}✅ Outputs OK${NC}"
echo ""

# Test 6: Check Files
echo -e "${BLUE}🔍 Test 6: Verify Created Files${NC}"
FILES_OK=0

if [ -f lambda_config.json ]; then
  echo -e "${GREEN}✅ lambda_config.json exists${NC}"
  ((FILES_OK++))
else
  echo -e "${RED}❌ lambda_config.json missing${NC}"
fi

if [ -f api_config.json ]; then
  echo -e "${GREEN}✅ api_config.json exists${NC}"
  ((FILES_OK++))
else
  echo -e "${RED}❌ api_config.json missing${NC}"
fi

if [ -f deployment_result.txt ]; then
  echo -e "${GREEN}✅ deployment_result.txt exists${NC}"
  ((FILES_OK++))
else
  echo -e "${RED}❌ deployment_result.txt missing${NC}"
fi

if [ $FILES_OK -eq 3 ]; then
  echo -e "${GREEN}✅ All files OK${NC}"
else
  echo -e "${RED}❌ Some files missing${NC}"
fi
echo ""

# Test 7: Verify File Contents
echo -e "${BLUE}🔍 Test 7: Verify File Contents${NC}"
if grep -q "devops-lab-test-function" lambda_config.json; then
  echo -e "${GREEN}✅ lambda_config.json valid${NC}"
else
  echo -e "${RED}❌ lambda_config.json invalid${NC}"
  exit 1
fi

if grep -q "localhost:8080" api_config.json; then
  echo -e "${GREEN}✅ api_config.json valid${NC}"
else
  echo -e "${RED}❌ api_config.json invalid${NC}"
  exit 1
fi

if grep -q "Lambda Function Deployment Result" deployment_result.txt; then
  echo -e "${GREEN}✅ deployment_result.txt valid${NC}"
else
  echo -e "${RED}❌ deployment_result.txt invalid${NC}"
  exit 1
fi
echo ""

# Test 8: Cleanup
echo -e "${BLUE}🔍 Test 8: Cleanup${NC}"
if terraform destroy -auto-approve > /dev/null 2>&1; then
  echo -e "${GREEN}✅ Cleanup OK${NC}"
else
  echo -e "${RED}⚠️  Cleanup warning (may be expected)${NC}"
fi
echo ""

echo "════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
echo "════════════════════════════════════════════════════════════"
