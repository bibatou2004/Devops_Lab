╔════════════════════════════════════════════════════════════╗
║  Lambda Function Deployment Result                        ║
╚════════════════════════════════════════════════════════════╝

Function Name: ${function_name}
API Endpoint:  ${api_endpoint}
Status:        ${status}
Timestamp:     ${timestamp}

Environment:
  Runtime:     nodejs18.x
  Memory:      128 MB
  Timeout:     30 seconds

API Gateway Configuration:
  Protocol:    HTTP
  Method:      GET
  Path:        /

Health Check:
  Endpoint:    ${api_endpoint}/
  Expected:    200 OK
  Message:     "Hello, World!"

Test Commands:
  curl ${api_endpoint}/
  curl ${api_endpoint}/name/DevOps
  curl ${api_endpoint}/add/5/3

═════════════════════════════════════════════════════════════
