# Distro - Orquestrador de automações

Documentação de utilização do orquestrador de automações para Python

## Tecnologias utilizadas
- Python
- Django
- RQ
- Redis
- Docker

---

## Configurações

### Arquivo config.cfg
Na pasta raiz do projeto temos que configurar o arquivo chamado *config.cfg* com as seguintes variáveis:

- task_retries: **Quantidade de vezes que um job irá repetir em caso de falha**
- modules_path: **Nome da pasta principal que você alocará suas automações/scripts**
- postgre_url: **URL de conexão com o postgres**

### Orquestrador
Para iniciar o orquestrador principal, basta executar o script *start_distro.bat* que se encontra na pasta raiz do projeto, ou iniciar o docker-compose manualmente.

As portas padrões de acesso serão:

- 7000: Serviço web do orquestrador
- 6379: Redis
- 9181: Dashboard do orquestrador

### Workers
**Nota: Os workers são feitos para serem executados nativamente apenas em sistema UNIX (Linux)**

Para configurar e iniciar um worker, primeiro precisamos de uma pasta com todos os nossos arquivos .py que desejamos executar (automações, scripts, etc...), é recomendado que essa pasta seja um repositório no GitHub para controle de versão. 

Obrigatoriamente essa pasta deve ter um arquivo \_\_init\_\_.py para o orquestrador entender como um módulo python e um requirements.txt com todos os módulos que sua automação/script irá usar e obrigatoriamente o módulo "rq", que irá ser responsável por iniciar o worker.

Segue abaixo um exemplo de requirements.txt:

```python
attrs==23.1.0
psycopg2==2.9.7
pycparser==2.21
pyodbc==4.0.39
PySocks==1.7.1
selenium==4.11.2
sniffio==1.3.0
urllib3==2.0.4
wsproto==1.2.0
rq==1.15.1
```

Após fazermos essas configurações, basta acessarmos a pasta dos nossos scripts e executarmos o comando abaixo:

```
rq worker --with-scheduler --url {redis_url} {queue}
```

Na variável "redis_url" iremos colocar a url de conexão para o redis que iniciamos usando o docker-compose, geralmente ficará no seguinte formato: **redis://<IP_DO_SEU_HOST>:6379/1**

Na variável "queue" iremos indicar qual o tipo de fila queremos que nosso worker atenda (low, default, high):

- low: Fila de baixa prioridade
- default: Fila padrão
- high: Fila de alta prioridade

Podemos também passar múltiplas filas, por exemplo, se eu inicio um worker para atender as filas de baixa prioridade e a fila padrão, meu comando ficaria da seguinte forma:

```
rq worker --with-scheduler --url {redis_url} low default
```

Podemos nomear os workers para melhor identificação no RQ Dashboard, por exemplo, se eu quiser nomear meu worker de "servidor02" meu comando ficaria:

```
rq worker --with-scheduler --url {redis_url} --name servidor02 low default
```

Seguindo os passos acima, já temos nosso worker funcionando e aguardando as tarefas serem agendadas pelo orquestrador principal.

**Nota: lembre-se que o orquestrador principal deve ter acesso a pasta com as mesmas automações/scripts que os workers, conforme configuramos o modules_path no início do orquestrador**

---

## Endpoints

### 1. GET - Listando módulos disponíveis - /scheduler/modules

Este endpoint recupera uma lista de todos os arquivos disponíveis na pasta definida no *modules_path* do orquestrador.

**Resposta**
- Código de Status: 200 (OK)
- Tipo de Conteúdo: `application/json`

Caso eu tenha apenas um arquivo chamado *hello_world.py* na pasta definida anteriormente, meu retorno será:
```json
[
    {
        "module": "hello_world"
    }
]
```

### 2. POST - Enfileirando uma task - scheduler/queue-task

Este endpoint coloca imediatamente a execução de uma task na fila do Redis.

**Body**
Aqui iremos mandar os parâmetros da task que eu quero executar:
- module: Arquivo onde está minha função
- function: Nome da minha função dentro do meu arquivo .py
- queue: Fila de prioridade em que eu quero enfileirar minha task

Se eu tenho dentro da minha pasta de automações um arquivo chamado *hello_world.py* e dentro desse arquivo eu tenho uma função chamada *send_hello_world*, que é a função que eu desejo que seja executada, minha requisição ficará da seguinte forma:

```json
{
    "module":"hello_world",
    "function":"send_hello_world",
    "queue":"default"
}
```

**Resposta**
- Código de Status: 201 (CREATED)
- Tipo de Conteúdo: `application/json`

```json
{
    "message": "task enqueued on default queue.",
    "task": "hello_world.send_hello_world"
}
```

### 3. POST - Agendando o enfileiramente de uma task - scheduler/schedule-task

Este endpoint irá agendar o enfileiramento de uma task

**Body**
Aqui iremos enviar os mesmos parâmetros enviados no endpoint anterior, com adição de mais 3 **opcionais**:

- seconds
- minutes
- hours

Esses parâmetros são inteiros que irão definir quanto tempo eu quero esperar para agendar a execução de uma tarefa, por exemplo, se eu desejo que a execução do meu *send_hello_world* seja enfileirada apenas daqui 2 horas, 10 minutos e 20 segundos, meu body ficaria da seguinte forma:

```json
{
    "module":"hello_world",
    "function":"send_hello_world",
    "queue":"default",
    "seconds": 20,
    "minutes": 10,
    "hours": 2
}
```

**Resposta**
- Código de Status: 201 (CREATED)
- Tipo de Conteúdo: `application/json`

```json
{
    "message": "task scheduled for 2 Hours, 10 Minutes and 20 Seconds from now on default queue.",
    "task": "hello_world.send_hello_world"
}
```

### 4. GET - Limpando a fila de exeução - scheduler/clean-queue
Este endpoint irá limpar (deletar) toda a fila de execução do redis que ainda não tenham sido executados por um worker.

**Resposta**
- Código de Status: 200 (OK)
- Tipo de Conteúdo: `application/json`

```json
{
    "message": "queue cleaned up"
}
```

## RQ Dashboard
O RQ Dashboard é um frontend simples para acompanhamento das tasks, workers e queues. Estará disponível na porta de execução 9181.

Documentação completa: https://github.com/Parallels/rq-dashboard