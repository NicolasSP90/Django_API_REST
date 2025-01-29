

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
python -m venv .venv
poetry init
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

O projeto irá utilizar os modelos

* Users - herdando *AbstractUser* para funções de validação, autenticação e definição de senhas, além de campos padronizados (como username, email, password...). Um usuário pode ter diversas contas.

* Accounts - Modelo para informações da conta. Cada conta é vinculada a um único usuário, mas pode estar vinculada a diversas transações.

* Transactions - Modelo para informações das transacões. Cada Transacão é vinculada a duas contas ('Origem' e 'Destino')

* AccountsTransactions - tabela intermediária para lidar com a relação ManytoMany das tabelas de *Accounts* e *Transactions*

![Diagrama Objetos](assets/Tables.png)

### Banco de dados

Definidos os objetos e as relações, os é possível criar uma migration. Antes disso, configurar a conexão com PostgreSQL. Garantir que o usuário tenha permissão para realizar a criação/modificação de tabelas.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("ENV_DB_NAME"),
        'USER': os.getenv("ENV_DB_USER"),
        'PASSWORD': os.getenv("ENV_DB_PASSWORD"),
        'HOST': os.getenv("ENV_DB_HOST"),
        'PORT': os.getenv("ENV_DB_PORT")
    }
}
```

Agora é possível criar as migration e realizar a criação das tabelas no banco.

```
python manage.py makemigrations
python manage.py migrate
```

### Definindo Superuser

Após definir o modelo em *api_rest/admin.py*, um superuser pode ser criado com:

```
python manage.py createsuperuser
```

Após isso o servidor pode ser inicializado para login como admin.

```
python manage.py runserver
```

O servidor pode ser acessado pelo endereço no terminal. Neste caso *http://127.0.0.1:8000/* e a url de admin em *http://127.0.0.1:8000/admin*

No postgreSQL o superuser criado se encontra na tabela *auth_users*

```
SELECT * FROM auth_user
```

### Serializers

Em *api_rest/serializers.py* estão definidas as estruturas de retorno de json dos objetos.

### Views

Em *api_rest/views.py* estão definidas as funções da api.
