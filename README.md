# Global-solution-Tech-de-bairro
Aplicação em Python com Oracle Database para gestão de alunos, CRUD, consultas estatísticas, trilhas de aprendizado e exportação JSON.

==🚀 Tech de Bairro

Sistema em Python com integração ao Oracle Database para cadastro, gestão e análise de alunos de projetos de capacitação tecnológica por bairro.

O projeto simula uma aplicação CRUD completa em terminal, com consultas obrigatórias, exportação de dados em JSON e trilhas de aprendizado personalizadas (Python, IA, Java, Frontend e Dados).

---

 📌 Funcionalidades

 👤 Gestão de Alunos (CRUD)

* Cadastrar aluno
* Listar todos os alunos
* Consultar aluno por ID
* Atualizar dados do aluno
* Excluir aluno

### 🔍 Consultas Obrigatórias

* Alunos **sem acesso à internet**
* Quantidade de alunos **por bairro**
* Distribuição por **faixa etária**

### 📤 Exportação

* Exportação completa dos dados e consultas em um único arquivo JSON:

  * `tech_de_bairro_export.json`

### 📚 Trilhas de Aprendizado

Cada aluno possui uma trilha associada:

* Python
* Inteligência Artificial
* Java
* Frontend
* Dados

Para cada trilha, o sistema exibe:

* 📘 E-book recomendado
* 🧩 Desafio mensal
* 💻 Equipamentos sugeridos

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Oracle Database**
* Biblioteca `oracledb`
* Manipulação de dados com `json`
* Validações com `re`

---

## 🗂️ Estrutura do Projeto

```
tech-de-bairro/
│
├── main.py
├── tech_de_bairro_export.json
└── README.md
```

---

## 🔐 Configuração do Banco de Dados

No início do código, configure as credenciais do Oracle:

```python
ORACLE_CONFIG = {
    "user": "SEU_USUARIO",
    "password": "SUA_SENHA",
    "dsn": "oracle.**.com.br:1521/ORCL"
}
```

⚠️ **Nunca publique suas credenciais reais em repositórios públicos.**

---

## ▶️ Como Executar

1. Instale as dependências:

```bash
pip install oracledb
```

2. Execute o sistema:

```bash
python main.py
```

3. Navegue pelo menu interativo no terminal.

---

## 📊 Exemplo de Menu

```
1. Cadastro de alunos
2. Trilha
3. Consultas
4. Exportar todas as consultas
5. Sair
```

---

Objetivo do Projeto

Este projeto foi desenvolvido com fins acadêmicos, focando em:

* Lógica de programação
* Integração com banco de dados
* Estruturação de código
* CRUD completo
* Consultas e relatórios

---

==👩‍💻 Autora

Giovana Souza Vieira
🎓 Análise e Desenvolvimento de Sistemas
💻 Desenvolvedora em formação | Full Stack

---

Projeto simples, funcional e com propósito social.
