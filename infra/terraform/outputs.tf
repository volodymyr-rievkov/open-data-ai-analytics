output "public_ip" {
  description = "Public IP адреса VM"
  value       = azurerm_public_ip.pip.ip_address
}

output "app_url" {
  description = "URL веб-інтерфейсу Streamlit"
  value       = "http://${azurerm_public_ip.pip.ip_address}:8501"
}

output "grafana_url" {
  description = "URL Grafana (admin / admin123)"
  value       = "http://${azurerm_public_ip.pip.ip_address}:3000"
}

output "prometheus_url" {
  description = "URL Prometheus"
  value       = "http://${azurerm_public_ip.pip.ip_address}:9090"
}

output "ssh_command" {
  description = "Команда для підключення до VM по SSH"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.pip.ip_address}"
}

output "cloud_init_log" {
  description = "Команда для перегляду логів cloud-init"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.pip.ip_address} 'sudo tail -f /var/log/cloud-init-output.log'"
}
