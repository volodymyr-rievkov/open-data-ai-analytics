output "public_ip" {
  description = "Public IP адреса VM"
  value       = azurerm_public_ip.pip.ip_address
}

output "app_url" {
  description = "URL веб-інтерфейсу Streamlit"
  value       = "http://${azurerm_public_ip.pip.ip_address}:8501"
}

output "ssh_command" {
  description = "Команда для підключення до VM по SSH"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.pip.ip_address}"
}
