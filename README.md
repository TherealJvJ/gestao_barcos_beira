# Sistema de Gestão de Barcos — INTRANSMAR Beira 🎣

Este projeto foi totalmente construído e codificado de acordo com os requisitos e regras de negócio da INTRANSMAR (Beira, Moçambique) e da pesca artesanal local.

## 📁 Estrutura do Projeto
- `core/` — Aplicação Django principal (models em português, views, forms, decorators e comandos).
- `core/services/` — Integração de serviços (MozeSMS, Gmail SMTP, PDFs com ReportLab).
- `gestao_barcos/` — Configurações do projeto Django (banco de dados, email, rotas).
- `templates/` — Templates HTML com tema marítimo (azul oceano, azul profundo, areia clara).
- `static/` — CSS marítimo premium e JavaScript com alertas SweetAlert2 e gráficos Chart.js.
- `mobile_app/` — Aplicação móvel Flutter completa pronta para consumo da API REST.

---

## 🛠️ Próximos Passos Obrigatórios (Executar localmente)

### 1. Instalação do PostgreSQL 16
Como a instalação local via terminal automático é bloqueada pelo UAC do Windows (exigência de privilégios de administrador), instale o PostgreSQL manualmente:
1. Descarregue o instalador do PostgreSQL 16 para Windows no site oficial da [EnterpriseDB](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads).
2. Siga o assistente de instalação:
   - **Password do superuser (`postgres`):** defina como `postgres` (para corresponder ao seu ficheiro `.env`).
   - **Porta:** 5432.
3. Abra a ferramenta **pgAdmin 4** (instalada juntamente com o PostgreSQL) ou utilize a linha de comandos (SQL Shell - psql) para criar a base de dados:
   ```sql
   CREATE DATABASE gestao_barcos_beira;
   ```

### 2. Configurar o Ambiente de Desenvolvimento Python
No seu terminal local (no diretório `E:\gestao_barcos_beira`), crie um ambiente virtual e instale as dependências:
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No PowerShell:
.\venv\Scripts\Activate.ps1
# No Prompt de Comando (CMD):
.\venv\Scripts\activate.bat

# Instalar dependências
pip install -r requirements.txt
```

### 3. Executar Migrações e Inicializar a Base de Dados
Com a base de dados criada e o ambiente virtual ativo:
```bash
# Gerar ficheiros de migração
python manage.py makemigrations core

# Aplicar migrações ao PostgreSQL
python manage.py migrate

# Criar utilizador Administrador principal do sistema
# (Introduza o e-mail, nome completo, telefone e palavra-passe quando solicitado)
python manage.py createsuperuser
```

### 4. Iniciar o Servidor Django
```bash
python manage.py runserver
```
Aceda ao sistema no seu browser através de: `http://127.0.0.1:8000/`.

---

## 📱 Aplicação Flutter (Mobile)
A aplicação móvel encontra-se na pasta `mobile_app/`. Para rodar ou compilar:

1. **Instalar o Flutter SDK via Puro (Já Instalado):**
   Como o gestor **Puro** já foi instalado no seu computador via `winget`, a instalação do Flutter é extremamente simples:
   - Feche e reabra o seu terminal (para carregar a nova variável `PATH`).
   - Execute o seguinte comando para descarregar e configurar o Flutter SDK estável:
     ```bash
     puro create meu-flutter stable
     ```
   - Defina essa versão como padrão global:
     ```bash
     puro global meu-flutter
     ```
   - O comando `flutter` ficará imediatamente ativo no seu terminal!

2. **Instalar dependências da app:**
   Navegue até a pasta da app móvel e instale as dependências:
   ```bash
   cd mobile_app
   flutter pub get
   ```
3. **Executar a app:**
   Altere o endereço IP no ficheiro `lib/services/api_service.dart` (substitua `10.0.2.2` pelo IP local do seu computador na rede Beira se testar em telemóvel real).
   Execute a app:
   ```bash
   flutter run
   ```

---

## 🔔 Teste de Notificações SMS (MozeSMS) e E-mails (Gmail)
1. Edite o ficheiro `E:\gestao_barcos_beira\.env` e preencha as credenciais da **MozeSMS** e o seu **Gmail SMTP** (com a senha de app de 16 caracteres gerada na segurança da sua conta Google).
2. Para testar o serviço automático de envio de alertas diários para documentos a expirar (licenças e vistorias), execute o comando Django:
   ```bash
   python manage.py verificar_alertas
   ```
