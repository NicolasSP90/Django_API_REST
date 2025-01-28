

# Projeto

Desenvolvimento de API Rest com Python e Django. Segue conjunto de tecnologias utilizadas:

* pyenv: gerenciados de versões do Python.
* venv: módulo nativo para criação do ambiente virtual
* poetry: gerenciador de dependências e bibliotecas do projeto
* django: framework web em Python para o desenvolvimento rápido de aplicações. 
* django REST Framework: framework construído sobre o Django, para criar APIs RESTful. 
* django-cors-headers: biblioteca para lidar com Cross-Origin Resource Sharing (CORS) em projetos Django.

O projeto foi dividido nas seguintes etapas:

[ ] Configuração do Ambiente
[ ] Definições do Framework
[ ] Objetos e Relacionamentos
[ ] Migrations e Banco de Dados
[ ] Requisições
[ ] Autenticação e JWT
[ ] Criação de Usuários e Login



## Configuração do Ambiente

* *pyenv* - Selecionada a versão do Python (3.13.1 - a mais recente dado que não existe necessidade explicita de versão);
* *venv* - Criação de ambiente virtual;
* *poetry* - Gerenciamento de pacotes e requerimentos;
* *python-dotenv* - Gerenciamento de variáveis de ambiente;
* *psycopg2-binary* - Conexão com banco PostgreSQL;
* *django[bcrypt]* - criptografia das senahs de usuários;

Segue configuração inicial:

```
pyenv local 3.13.1
```

```
python -m venv .venv
```

```
poetry init
```

```
poetry add django
poetry add djangorestframework
poetry add django-cors-headers
poetry add python-dotenv
poetry add psycopg2-binary
poetry add django[bcrypt]
```

## Django

Initializando o projeto com os comandos:

```
django-admin startproject api_root .
py manage.py startapp api_rest
```

Alterar o arquivo */api_root/settings*:
* Em INSTALLED_APPS adicionar:
    * 'rest_framework', # REST framework adicionado
    * 'corsheaders', # corsheaders adicionado
    * 'api_rest' # aplicação

* Em MIDDLEWARE adicionar:
    * 'corsheadres.middleware.CorsMiddleware' 

* Adicionar no final (alterar/adicionar o endereço de produção posteriormente - AWS, GCP, Azure) :
    * CORS_ALLOW_ORIGINS = ['https://localhost:8080']

* Pode ser necessário adicionar o seguinte para acesso de diversos locais:
    * CORS_ORIGIN_ALLOW_ALL = True

### Objetos e Relacionamentos

### Banco de dados


```
python manage.py makemigrations
python manage.py migrate
```
