# FinanceFlow 💰

FinanceFlow é uma aplicação web completa de gestão financeira pessoal e empresarial construída com Python, focada em simplicidade, segurança e integração de dados.

## Funcionalidades Principais

* 🔒 **Sistema de Autenticação Seguro**: Proteção total dos dados usando criptografia de senha (Flask-Login e Werkzeug).
* 📊 **Dashboard Dinâmico**: Resumos financeiros instantâneos e gráficos gerados por Chart.js.
* 📅 **Filtros Temporais Inteligentes**: Acompanhe as despesas focadas no Mês atual ou tenha uma visão panorâmica do Ano Inteiro.
* 🗑️ **Gestão Completa de Dados**: Cadastre, **edite** e exclua lançamentos incorretos com precisão de Data e Hora.
* 📈 **Integração com Business Intelligence**: Exportação otimizada via *Pandas* em CSV limpo e compatível nativamente com Microsoft Power BI.
* ⚡ **Alta Performance**: Banco de dados indexado (SQLite/SQLAlchemy) para extrações anuais rápidas.

## Stack de Tecnologias

* **Backend**: Python 3, Flask, Flask-Login
* **Banco de Dados**: SQLite, SQLAlchemy ORM
* **Análise de Dados**: Pandas
* **Frontend**: HTML5, CSS3, Vanilla Javascript, Chart.js

## Como Executar Localmente

### Pré-requisitos
* Python 3.8+ instalado.

### Passos da Instalação

1. Clone o repositório:
```bash
git clone https://github.com/SeuUsuario/FinanceFlow.git
cd FinanceFlow
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
# No Windows
.\.venv\Scripts\Activate.ps1
# No Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências requeridas:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
python app.py
```

5. Acesse o sistema pelo navegador em `http://localhost:5000`.
   - **Usuário Padrão**: admin
   - **Senha Padrão**: admin123

## Estrutura do Projeto

* `app.py`: Configuração central e inicialização.
* `models.py`: Arquitetura do Banco de Dados (ORM).
* `routes/`: Endpoints modulares (Transações, Dashboard, Autenticação).
* `templates/`: Interfaces HTML modulares (Jinja2).
* `static/`: Ativos do frontend (CSS, JS).

---
Desenvolvido como projeto de portfólio.
