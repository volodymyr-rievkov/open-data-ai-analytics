# Лабораторна робота №1

## з предмету "Середовище та компоненти розробки у моделюванні та аналізі даних"

### Тема: Використання системи контролю версій Git

### Мета:
- Навчитися працювати з відкритими даними (портал data.gov.ua), виконувати їх завантаження, очищення, аналіз та візуалізацію.

- Опанувати професійний підхід до розробки через Git: створення гілок під кожну задачу (feature-branches), злиття (merge), створення запитів на злиття (Pull Requests), тегування версій та вирішення конфліктів.

- Навчитися правильно організовувати файлову структуру проєкту (src, data, notebooks, reports).

## Джерело даних
Дані отримано з Єдиного державного порталу відкритих даних: https://data.gov.ua/dataset/national-teams

## Питання та гіпотези для аналізу
1. **Регіональне лідерство:** Які області України та спортивні товариства (ФСТ) забезпечують найбільшу кількість спортсменів до національних збірних?
2. **Ефективність планування:** Чи існує сильна кореляція між "запланованим результатом" та "результатом на поточний сезон" (наскільки реалістично тренери оцінюють потенціал)?
3. **Віковий та кваліфікаційний профіль:** Який середній вік спортсмена у збірній та як розподіляються спортивні розряди (МСУ, МСУМК) залежно від виду спорту?

## Скрипт data_quality_analysis аналізує якість даних, типізує їх та заповнює значення Nan.(тут станеться конфлікт)

## Скрипт data_research дає відповіді на наші питання та гіпотези. (тут станеться конфлікт)


# Лабораторна робота №3

## з предмету "Середовище та компоненти розробки у моделюванні та аналізі даних"

### Тема: Контейнеризація модулів проєкту за допомогою Docker

### Мета:
 - Опанувати базові принципи контейнеризації застосунків та навчитися запускати окремі модулі проєкту в Docker-середовищі. Закріпити навички побудови багатомодульного проєкту, роботи з Dockerfile, Docker Compose, томами, мережами та контейнерною взаємодією між сервісами.

### Інструкція:
1. Запустити сервіс
2. Перейти за посиланням http://localhost:8501 для перегляду результатів

### Команда для запуску сервісу
```bash
docker-compose up --build
```

### Команда запуску self-hosted runner
```bash
cd ../actions-runner
./run.cmd
```

# Лабораторна робота №4

### Інструкція щодо запуску в Azure
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
git clone https://github.com/volodymyr-rievkov/open-data-ai-analytics
cd open-data-ai-analytics/infra/terraform
terraform init
terraform apply -auto-approve [OPTIONAL] -var="repo_branch=feature/grafana-monitoring"
ssh azureuser@public_ip
sudo tail -f /var/log/cloud-init-output.log
```
Чекаємо на `cloud.init` та переходимо за лінкою: `public_ip`


# Лабораторна робота №5

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
git clone https://github.com/volodymyr-rievkov/open-data-ai-analytics
cd open-data-ai-analytics/infra/terraform
terraform init
terraform apply -auto-approve [OPTIONAL] -var="repo_branch=feature/grafana-monitoring"
ssh azureuser@public_ip
sudo tail -f /var/log/cloud-init-output.log
```
Чекаємо на `cloud.init` та переходимо за лінкою: `public_ip`

Порт 3000 - графана (id vm monitoring 1860, id containers monitoring 14282)
Порт 9090 - прометеус
Порт 8501 - web streamlit


# Лабораторна робота №6

### Тема: Ознайомлення із практиками GitOps

### Інструкція щодо запуску в Azure
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
git clone https://github.com/volodymyr-rievkov/open-data-ai-analytics
cd open-data-ai-analytics/infra/terraform
terraform init
terraform apply -auto-approve
ssh azureuser@public_ip
sudo tail -f /var/log/cloud-init-output.log
```

Чекаємо на завершення `cloud-init` (~15 хвилин) та переходимо за посиланнями:

| Сервіс | Порт | Опис |
|--------|------|------|
| Streamlit (Docker Compose) | 8501 | Веб-інтерфейс застосунку |
| Streamlit (Kubernetes) | 30501 | Веб-інтерфейс через k3s |
| Grafana | 3000 | Моніторинг (admin / admin123) |
| Prometheus | 9090 | Метрики |
| Argo CD | 30443 | GitOps UI (HTTPS) |

### Отримати пароль Argo CD
```bash
KUBECONFIG=/home/azureuser/.kube/config kubectl get secret argocd-initial-admin-secret \
  -n argocd -o jsonpath="{.data.password}" | base64 -d
```

### Перевірка кластера
```bash
export KUBECONFIG=/home/azureuser/.kube/config
kubectl get nodes
kubectl get pods -n argocd
kubectl get pods -n open-data-ai
```

### Демонстрація автосинку (зміна кількості реплік)
```bash
# Змінити replicas в gitops/app/deployment.yaml
# Потім запушити в main
git add gitops/app/deployment.yaml
git commit -m "demo: scale to 2 replicas"
git push origin main
# Argo CD автоматично застосує зміни через ~3 хвилини
```

### Демонстрація rollback
```bash
git revert HEAD
git push origin main
# Argo CD автоматично повертає попередній стан
```

### Після демонстрації — видалити ресурси
```bash
cd open-data-ai-analytics/infra/terraform
terraform destroy -auto-approve
```
