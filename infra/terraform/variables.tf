variable "resource_group_name" {
  description = "Назва Resource Group в Azure"
  type        = string
  default     = "open-data-ai-rg"
}

variable "location" {
  description = "Azure регіон"
  type        = string
  default     = "polandcentral"
}

variable "prefix" {
  description = "Префікс для іменування ресурсів"
  type        = string
  default     = "open-data-ai"
}

variable "vm_size" {
  description = "Розмір VM (Standard_B1ms = 1vCPU / 2GB, достатньо для студентського кредиту)"
  type        = string
  default     = "Standard_B2s_v2"
}

variable "admin_username" {
  description = "Ім'я адміністратора VM"
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key_path" {
  description = "Шлях до публічного SSH-ключа"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "repo_branch" {
  description = "Гілка репозиторію для клонування"
  type        = string
  default     = "main"
}
