# Instruções para executar o projeto

Esse é um projeto que extrai um documento em PDF para um banco RAG, e com isso envia os embedded para que a IA consiga tirar das informações armazenadas na base, a resposta necessária para responder o usuário.

### Requisitos
- Esse é um projeto desenvolvido com Python, logo é necessário que tenha python instalado na máquina
- Como vamos rodar o PgVector via Docker, então é necessário que o docker esteja instalado: https://www.docker.com/
- Antes de executar o projeto é preciso que uma instância do PgVector rodando na sua máquina
- Definir as variáveis de ambiente no arquivo .env
- <strong> Para o caso das LLM </strong> é preciso definir o OpenAi ou Gemini, caso haja os dois, o aplicativo vai optar pela OpenAi
- Colocar um documento pdf na raiz do projeto
- Inserir os comandos informados na secção de comandos para preparar e rodr o projeto

### Variáveis de ambiente
( Todas as variáveis do Postgree, são encontradas no compose.yml)
- POSTGRES_URL:  HOST do conteiner; e.g.:localhost:5432
- POSTGRES_USER: -
- POSTGRES_PASSWORD: -
- POSTGRES_DB: -
- TABLE_NAME: Fica a seu critério o nome da tabela, no meu caso foi "doc"
- GEMINI_API_KEY : É necessário gerar uma chave da Gemini na plataform de API deles (https://aistudio.google.com/app/apikey)
- OPEN_API_KEY: Mesmo da Gemini, só que para o OpenAI (https://platform.openai.com/login?next=%2Fapi-keys)
- PDF_PATH : caso não queira a raiz do projeto, pode definir um lugar mais apropriado

### Executando o projeto 

1. Primeira parte é levantar um contêiner do PgVector, para que a aplicação tenha infraestrutura
   <br> <strong> 1.1 </strong> executar o comando "docker compose up" na raiza do projeto 
2.  Assim que a instância do PgVector estiver 100%, podemos construir o ambiente para execução do projeto:
   <br> <strong> 2.1 </strong> O projeto já possuí uma pasta "venv" com o ambiente virtual, caso esteja em um OS windows, usar o comando cmd: "<pasta do venv>\Scripts\activate.bat"; powershell:"<venv>\Scripts\Activate.ps1" . No linux, é "source venv/bin/activate"
   <br> <strong> 2.2 </strong> executar o comando "pip install -r requirements.txt" na raiz do projeto
3. Para alimentar o nosso RAG com o documento pdf, executar o comando:
   <br> <strong> 3.1 </strong> executar o comando python3 ./src/ingest.py na raiz do projeto. 
4.  Para executar o projeto:
   <br> <strong> 3.1 </strong> executar o comando python3 ./src/chat.py na raiz do projeto. Assim que executar a aplicação vai solicitar uma entrad de texto, que no caso é a pergunta que será feita para a IA responder, junto com as informações do RAG
