# Sistema de Gestao de Embarcacoes Artesanais — INTRANSMAR Beira

Trabalho de Conclusao de Curso (TCC) que apresenta o desenvolvimento de um sistema web e movel para a gestao e licenciamento de embarcacoes artesanais na Delegacao da Beira da INTRANSMAR (Instituto Nacional de Transportes Maritimos, Fluviais e Lacustres), Mocambique.

O sistema foi construido de acordo com os requisitos e regras de negocio da INTRANSMAR e da pesca artesanal local, abrangendo o registo de embarcacoes, emissao de licencas de navegacao e titulos de propriedade, vistorias, notificacoes automaticas (SMS e E-mail) e geracao de documentos em PDF.

## Tecnologias Utilizadas

| Camada         | Tecnologia                        |
|----------------|-----------------------------------|
| Backend        | Django 5.x + Django REST Framework |
| Base de Dados  | PostgreSQL 16                     |
| Frontend Web   | HTML5, CSS3, JavaScript (Chart.js, SweetAlert2) |
| App Movel      | Flutter (Dart)                    |
| SMS            | MozeSMS API REST                  |
| E-mail         | Gmail SMTP                        |
| PDF            | ReportLab                         |

## Estrutura do TCC

```
gestao_barcos_beira/
  core/                  -- Aplicacao Django principal (models, views, forms, decorators)
    management/commands/  -- Comandos automaticos (verificar_alertas)
    services/             -- Servicos de integracao (SMS, E-mail, PDF)
    views/                -- Views separadas por perfil (admin, intransmar, pescador, api)
  gestao_barcos/          -- Configuracoes do projecto Django (base de dados, rotas)
  templates/              -- Templates HTML com tema maritimo
  static/                 -- CSS, JavaScript e recursos estaticos
  mobile_app/             -- Aplicacao movel Flutter
    lib/views/            -- Ecras da aplicacao movel
    lib/services/         -- Servico de comunicacao com a API REST
    lib/theme/            -- Tema visual (TemaMaritimo)
```

## Funcionalidades Principais

- Registo e aprovacao de embarcacoes artesanais
- Emissao de Licencas de Navegacao (validade anual) e Titulos de Propriedade (permanente)
- Geracao automatica de documentos PDF com marca de agua e logotipo
- Notificacao automatica via SMS (MozeSMS) e E-mail ao pescador quando um documento e emitido
- Alertas automaticos de expiracao de licencas e vistorias (configuravel pelo administrador)
- Painel de controlo com graficos e estatisticas (Chart.js)
- Tres perfis de utilizador: Pescador, INTRANSMAR e Administrador
- Aplicacao movel Flutter para consulta de embarcacoes e documentos pelo pescador
- Recuperacao de palavra-passe via e-mail (web e movel)

---

## Instalacao e Configuracao

### 1. Requisitos

- Python 3.10 ou superior
- PostgreSQL 16
- Flutter SDK (para a aplicacao movel)
- Conta Gmail com senha de aplicacao (para envio de e-mails)
- Conta MozeSMS com credenciais de API (para envio de SMS)

### 2. Base de Dados

Instale o PostgreSQL e crie a base de dados:

```sql
CREATE DATABASE gestao_barcos_beira;
```

### 3. Ambiente de Desenvolvimento Python

```bash
# Criar ambiente virtual
python -m venv .venv

# Activar ambiente virtual (PowerShell)
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configuracao do Ficheiro .env

Copie o ficheiro de exemplo e preencha com as suas credenciais:

```bash
copy .env.example .env
```

Preencha os campos:
- SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD (PostgreSQL)
- MOZESMS_API_KEY, MOZESMS_API_SECRET, MOZESMS_SENDER_ID (MozeSMS)
- EMAIL_HOST_USER, EMAIL_HOST_PASSWORD (Gmail SMTP)

### 5. Migracoes e Utilizador Administrador

```bash
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
```

### 6. Iniciar o Servidor

```bash
python manage.py runserver
```

Aceda ao sistema em: http://127.0.0.1:8000/

---

## Aplicacao Movel (Flutter)

A aplicacao movel encontra-se na pasta `mobile_app/`.

### Instalacao

```bash
cd mobile_app
flutter pub get
```

### Execucao em dispositivo fisico (via USB)

1. Ligue o telemovel ao computador por cabo USB.
2. Active a ponte de comunicacao:
   ```bash
   adb reverse tcp:8000 tcp:8000
   ```
3. Inicie a aplicacao:
   ```bash
   flutter run
   ```

---

## Alertas Automaticos de Expiracao

O sistema possui um comando Django que verifica automaticamente todas as licencas e vistorias proximas da data de expiracao e envia notificacoes (SMS e E-mail) aos proprietarios.

O administrador configura os parametros de alerta (dias de antecedencia e canal de envio) atraves do painel web, na seccao "Configuracao de Alertas".

Para executar a verificacao manualmente:

```bash
python manage.py verificar_alertas
```

---

## Autor

Joaquim Arone — Trabalho de Conclusao de Curso
