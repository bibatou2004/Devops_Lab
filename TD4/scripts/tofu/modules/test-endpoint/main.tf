# Module test-endpoint - Teste les endpoints HTTP
data "http" "test_endpoint" {
  url = var.endpoint
  
  # Ignorer les erreurs SSL pour le test
  insecure = true
  
  request_headers = {
    Accept = "application/json"
  }
}

# Ajouter une delay pour attendre que l'endpoint soit prêt
resource "null_resource" "wait_for_endpoint" {
  provisioner "local-exec" {
    command = "sleep 5"
  }
}
