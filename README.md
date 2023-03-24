<!--
*** Obrigado por estar vendo o nosso README. Se você tiver alguma sugestão
*** que possa melhorá-lo ainda mais dê um fork no repositório e crie uma Pull
*** Request ou abra uma Issue com a tag "sugestão".
*** Obrigado novamente! Agora vamos rodar esse projeto incrível :D
-->

<!-- PROJECT SHIELDS -->

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://theplumbers.com.br/">
    <img src="https://avatars.githubusercontent.com/u/100875314?s=200&v=4" alt="Logo">
  </a>

  <h3 align="center">https://theplumbers.com.br/</h3>
</p>

<!-- TABLE OF CONTENTS -->

# Tabela de Conteúdo

- [Tabela de Conteúdo](#tabela-de-conte%C3%BAdo)
- [Sobre o Projeto](#sobre-o-projeto)
- [Feito Com](#feito-com)
- [Fluxo de versionamento](#fluxo-de-versionamento)
- [Começando](#come%C3%A7ando)
  - [Pré-requisitos](#pr%C3%A9-requisitos)
  - [Instalação do cluster](#instala%C3%A7%C3%A3o-do-cluster)
  - [Instalação das ferramentas](#instala%C3%A7%C3%A3o-das-ferramentas)
  - [Executando o projeto](#executando-o-projeto)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
  - [Edição](#edi%C3%A7%C3%A3o)
- [Contribuição](#contribui%C3%A7%C3%A3o)
- [Licença](#licen%C3%A7a)
- [Contato](#contato)

<!-- ABOUT THE PROJECT -->

# Sobre o Projeto


Esse projeto tem como propósito realizar uma solução para o desafio do workshop construindo seu próprio Data Lakehouse usando o Delta Lake. [Link do desafio aqui!](https://github.com/GersonRS/ws-delta-lake-deep-dive/tree/main/challenge)

O projeto aqui detalhado tem como propósito criar uma POC (prova de conceito) única e exclusivamente afim de solucionar o desafio, independentemente das tecnologias utilizadas.

Este projeto visa a criação de um pipeline de dados que usa a arquitetura do medalhão [Bronze, Silver & Gold], que possa ser utilizado como uma POC, visto que o processo de criação e configuração de um pipeline de dados de um projeto usando este tipo de arquitetura pode gerar certa complexidade e muitas vezes até erros que atrasam o processo, atrapalhando assim o fluxo de desenvolvimento.

# Fluxo de versionamento:
Projeto segue regras de versionamento [gitflow](https://www.atlassian.com/br/git/tutorials/comparing-workflows/gitflow-workflow).

# Feito Com

Abaixo segue o que foi utilizado na criação deste projeto:

- [ArgoCD](https://argo-cd.readthedocs.io/en/stable/) - Argo CD, é uma ferramenta declarativa que usa a abordagem GitOps para implantar aplicações no Kubernetes, ele pode ser usado para gerenciar várias aplicações em diferentes clusters Kubernetes a partir de um único ponto. Ele pode se conectar a repositórios git públicos e privados, é gratuito, tem o código fonte aberto, é um projeto incubado pela CNCF, possui uma interface web de visualização e gerenciamento dos recursos, mas também pode ser configurado via linha de comando;
- [Redux](https://redux.js.org/) - O Redux é um contêiner de estado previsível para aplicativos JavaScript. Ele ajuda você a escrever aplicativos que se comportam consistentemente, executados em diferentes ambientes (cliente, servidor e nativo) e são fáceis de testar;
  - [Redux Saga](https://redux-saga.js.org/) - O redux-saga é uma biblioteca que tem como objetivo tornar os efeitos colaterais dos aplicativos mais fáceis de gerenciar, mais eficientes de executar, fáceis de testar e melhores em lidar com falhas;
- [React Navigation](https://reactnavigation.org/) - O React Navigation surgiu da necessidade comunidade do React Native de uma navegação de forma fácil de se usar, e escrita toda em JavaScript;

<!-- GETTING STARTED -->

# Começando

Para conseguir utilizar o projeto, seja através de um ambiente em cloud ou um cluster local, siga os passos abaixo.

## Pré-requisitos

Antes de seguirmos para as configurações e uso da solução do desafio, é ideal que você tenha o ambiente configurado para criar, testar e executar o projeto, para isso você pode seguir o guia abaixo:

### instalação do cluster

Primeiramente precisamos montar um ambiente com um cluster kubernetes local para que possamos executar nossa aplicação e execução do pipeline de dados.

Para esta POC usaremos o cluster de kubernetes **[minikube](https://minikube.sigs.k8s.io/docs/)**. Para instalar o minikube basta seguir [este guia de instalação](https://minikube.sigs.k8s.io/docs/start/).

Também usaremos o **[helm](https://helm.sh/)** para nos auxiliar na instalação de algumas aplicações. Para instalar o helm [siga este guia](https://helm.sh/docs/intro/install/).

Após estes dois pre-requisitos instalados é hora de iniciar o nosso cluster minikube:
> para que ocorra tudo bem é aconselhavel usar um cluster de no minimo 8Gb e 2 CPUs
```
minikube start --memory=8000 --cpus=2
```

> Para que alguns serviços sejam acessiveis via loadbalancer no minikube, é necessario que você use o [tunelamento do minikube](https://minikube.sigs.k8s.io/docs/handbook/accessing/#example-of-loadbalancer).
> Para isto abra uma nova aba do seu terminal e digite o seguinte commando:
>
>`minikube tunnel`
>
> Com isto o seu ambiente esta pronto para receber acessos via loadbalancer

### Instalação das ferramentas

Depois do ambiente inicializado será necessario instalar algumas aplicações que serão responsaveis por manter e gerenciar nosso pipeline de dados.

Estando conectado em um cluster Kubernetes, execute os seguintes comandos para criar todos os namespaces necessarios:

```sh
kubectl create namespace orchestrator
kubectl create namespace database
kubectl create namespace ingestion
kubectl create namespace processing
kubectl create namespace datastore
kubectl create namespace deepstorage
kubectl create namespace cicd
kubectl create namespace app
kubectl create namespace management
kubectl create namespace misc
```

Instale o argocd que será responsavel por manter nossas aplicações:
```sh
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm install argocd argo/argo-cd --namespace cicd --version 5.27.1
```

Altere o service do argo para loadbalancer:
```sh
# create a load balancer
kubectl patch svc argocd-server -n cicd -p '{"spec": {"type": "LoadBalancer"}}'
```

Em seguida instale o argo cli para fazer a configuração do repositorio:
```sh
sudo curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo chmod +x /usr/local/bin/argocd
```
Em seguida armazene o ip atribiudo para acessar o argo e faça o login no argo, com os seguintes comandos:
```sh
ARGOCD_LB=$(kubectl get services -n cicd -l app.kubernetes.io/name=argocd-server,app.kubernetes.io/instance=argocd -o jsonpath="{.items[0].status.loadBalancer.ingress[0].ip}")

# get password to log into argocd portal
# argocd login 192.168.0.200 --username admin --password UbV0FdJ2ZNCD8kxU --insecure
kubectl get secret argocd-initial-admin-secret -n cicd -o jsonpath="{.data.password}" | base64 -d | xargs -t -I {} argocd login $ARGOCD_LB --username admin --password {} --insecure
```
> caso queira ver o password do argo para acessar a interface web execute este comando: `kubectl get secret argocd-initial-admin-secret -n cicd -o jsonpath="{.data.password}" | base64 -d`

Uma vez feita a autenticação não é necessario adicionar um cluster, pois o argo esta configurado para usar o cluster em que ele esta instalado, ou seja, o cluster local ja esta adicionado como **`--in-cluster`**, bastando apenas adicionar o seu repositorio com o seguinte comando:

```sh
argocd repo add git@github.com:GersonRS/big-data-on-k8s.git --ssh-private-key-path ~/.ssh/id_ed25519 --insecure-skip-server-verification
```

> Lembrando que para este comando funcionar é necessario que você tenha uma `chave ssh` configurada para se conectar com o github no seu computador. Caso não tenha, use [este guia](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) para criar uma e [adiciona-la ao github](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

Agora é hora de adicionar as outras ferramentas necesarias para o nosso pipeline de dados. E para isto precisamos criar `secrets` para armazenar senhas e informações censiveis, que  sejam acessiveis pelas aplicações e processos do **`Spark`**, por isso é necessario que eles estejam no namespace onde esta rodando a aplicação e também no namespace processing, onde será executado os processos do `spark`. Então para isto podemos usar o **[Reflactor](https://github.com/EmberStack/kubernetes-reflector)**, que faz a replicação dos secrets nos namespaces que precisamos e não há a necessidade de re-criar os secrets em namespaces diferentes, e para isto execute este comando:

```sh
kubectl apply -f manifests/management/reflector.yaml
```

> Antes de executar os comando você pode alterar os secrets dos arquivos localizados na pasta `secrets/`, caso queira mudar os passwords de acessos aos databases e storage

Após o reflator esta em funcionamento, execute o comando que cria os secrets nos namespaces necessarios: 

```sh
# secrets
kubectl apply -f manifests/misc/secrets.yaml
```

> Caso não queira instalar o Reflactor para automatizar o processo de criar o secret em varios namespaces diferentes, você pode faze manualmente a replicação do secret para outro namespace executando este comando: 
`kubectl get secret minio-secrets -n deepstorage -o yaml | sed s/"namespace: deepstorage"/"namespace: processing"/| kubectl apply -n processing -f -`

Uma vez que, os secrets estejam configurados podemos começar instalando os databases e storage do nosso pipeline de dados com o seguinte comando:

```sh
# databases
kubectl apply -f manifests/database/postgres.yaml
# deep storage
kubectl apply -f manifests/deepstorage/minio.yaml
```

E por fim instale o Spark e o Airflow, juntamente com suas permições para executar os processos spark, executando os seguintes comandos:

```sh
# add & update helm list repos
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm repo add apache-airflow https://airflow.apache.org/
helm repo update
```

```sh
# processing
kubectl apply -f manifests/processing/spark.yaml
```

Antes de instalar o airflow é preciso atender um certo requisito, que é criar um secret contendo a sua `chave ssh` para o airflow baixar as `DAGs` necessarias atraves do gitSync. é possivel criar com o seguinte comando:

> Lembrando que para isto você deve ter a `chave ssh` configurada em sua maquina.

```sh
kubectl create secret generic airflow-ssh-secret --from-file=gitSshKey=$HOME/.ssh/id_ed25519 -n orchestrator
```
<!-- ```sh 
eval $(minikube docker-env)
docker build -f images/airflow/dockerfile images/airflow/ -t airflow:0.1
``` -->

```sh
# orchestrator
kubectl apply -f manifests/orchestrator/airflow.yaml
```

Em seguida instale as configurações de acesso:

```sh
kubectl apply -f manifests/misc/access-control.yaml
```

Com isto, temos o ambiente de desenvolvimento e de execução instalado e pronto.

### Executando o projeto


Antes de tudo é preciso ter uma `imagem spark` que contenha todos os jars necessarios para a execução do nosso pipeline e para criar uma imagem spark com estas especificações execute:

```sh
eval $(minikube docker-env)
docker build --no-cache -f images/spark/dockerfile images/spark/ -t spark:0.1
```
Neste projeto esta sendo usada a versão 3.3.2 do spark e 2.2.0 do delta, juntamente com todas as suas libs e jars nas versões compativeis seguindo as compatibilidades do delta [neste link](https://docs.delta.io/latest/releases.html) e neste link.

Apos a image spark esta criada abra a UI web do airflow. Caso não saiba qual foi o ip atribuido ao webserver do airflow execute o comando a seguir para descobrir se ip:
```sh
kubectl get services -n orchestrator -l component=webserver,argocd.argoproj.io/instance=airflow -o jsonpath="{.items[0].status.loadBalancer.ingress[0].ip}"
```

Uma vez que esteja na UI do airflow ative o pipeline de dados `pipeline-delta-lake-deep-dive-complete` e veja a magia acontecer. Ou se preferir você também pode executar cada etapa separadamene seguindo é claro a sequencia:
  * `ingestion-from-local-data-file-to-bronze-tables`
  * `transformation-and-enrichment-from-bronze-to-silver`
  * `delivery-data-from-silver-to-gold`

caso não deseje executar o pipeline pelo airflow, você pode executar o pipeline de dados executando os seguintes comandos em sequencia:
```sh
kubectl apply -f dags/spark_jobs/ingestion_from_local_data_file_to_bronze_tables.yaml -n processing
kubectl apply -f dags/spark_jobs/transform_and_enrichment_from_bronze_to_silver.yaml -n processing
kubectl apply -f dags/spark_jobs/delivery_data_from_silver_to_gold.yaml -n processing
```

Para verificar os arquivos no `data lakehouse` acesse a UI do `minio` e use as credenciais de acesso encontradas no aquivo *[minio-secrets.yaml](/secrets/minio-secrets.yaml)* na pasta *[secrets](/secrets/)*. Caso não saiba o ip atribuido ao minio execute:
```sh
kubectl get services -n deepstorage -l app.kubernetes.io/name=minio -o jsonpath="{.items[0].status.loadBalancer.ingress[0].ip}"
```
Caso queira pegar as credenciais de acesso do `minio`, execute:
```sh
echo "user: $(kubectl get secret minio-secrets -n deepstorage -o jsonpath="{.data.root-user}" | base64 -d)"
echo "password: $(kubectl get secret minio-secrets -n deepstorage -o jsonpath="{.data.root-password}" | base64 -d)"
```

## Pipeline Spark

Para este desafio foi escolhida 4 conjunto de dados **(`user`, `subscription`, `credit_card` e `movies`)**.
Os codigos spark foram escritos em `python` ***(Pyspark)*** e adicionados a uma [imagem docker](images/spark/dockerfile). Optei colocar todos os meus códigos spark na mesma `imagem`, pela simplicidade de desenvolver e explicar. Apesar de que este pode não ser a melhor pratica para esse tipo de problema(mas funciona).

Os dados da **`landing`** disponibilizados pelo desafio, também foram incluidos na `imagem`, os quais são transformados em **tabelas `delta`** em um `lakehouse` criado no `minio`. Sei que esta não foi a melhor pratica, mas esta também foi uma escolha pela simplicidade de replicação do projeto *(e minha falta de tempo de colocar no bucket)*.

### Carregando os dados na **`Bronze`**

[A primaira etapa do pipeline](/images/spark/ingestion_to_bronze.py), consiste em pegar os dados da `landing` (que estão na [imagem](/images/spark/dockerfile)) e transforma-los em `tabelas` **`delta`** em um **`lakehouse`**. Além disso são adicionados informações para analises posteriores como por exemplo: `ingestion_time`, `file_size` e dentre outros. É possivel ver todos as informações adicionais nas linhas `56-63` do arquivo [ingestion_to_bronze.py](/images/spark/ingestion_to_bronze.py).

Como dito anteriormente foram escolhidos os dados de `user`, `subscription`, `credit card` e `movies`, segue o schema das tabelas **`delta`** de cada um apos a ingestão da `landing` para a **`bronze`**:

```sh
user
 |-- address: struct (nullable = true)
 |    |-- city: string (nullable = true)
 |    |-- coordinates: struct (nullable = true)
 |    |    |-- lat: double (nullable = true)
 |    |    |-- lng: double (nullable = true)
 |    |-- country: string (nullable = true)
 |    |-- state: string (nullable = true)
 |    |-- street_address: string (nullable = true)
 |    |-- street_name: string (nullable = true)
 |    |-- zip_code: string (nullable = true)
 |-- avatar: string (nullable = true)
 |-- credit_card: struct (nullable = true)
 |    |-- cc_number: string (nullable = true)
 |-- date_of_birth: string (nullable = true)
 |-- dt_current_timestamp: long (nullable = true)
 |-- email: string (nullable = true)
 |-- employment: struct (nullable = true)
 |    |-- key_skill: string (nullable = true)
 |    |-- title: string (nullable = true)
 |-- first_name: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- id: long (nullable = true)
 |-- last_name: string (nullable = true)
 |-- password: string (nullable = true)
 |-- phone_number: string (nullable = true)
 |-- social_insurance_number: string (nullable = true)
 |-- subscription: struct (nullable = true)
 |    |-- payment_method: string (nullable = true)
 |    |-- plan: string (nullable = true)
 |    |-- status: string (nullable = true)
 |    |-- term: string (nullable = true)
 |-- uid: string (nullable = true)
 |-- user_id: long (nullable = true)
 |-- username: string (nullable = true)
 |-- ingestion_time: timestamp (nullable = false)
 |-- source_system: string (nullable = false)
 |-- user_name: string (nullable = false)
 |-- ingestion_type: string (nullable = false)
 |-- base_format: string (nullable = false)
 |-- file_size: integer (nullable = false)
 |-- rows_written: integer (nullable = false)
 |-- schema: string (nullable = false)
```
```sh
subscription
 |-- dt_current_timestamp: long (nullable = true)
 |-- id: long (nullable = true)
 |-- payment_method: string (nullable = true)
 |-- payment_term: string (nullable = true)
 |-- plan: string (nullable = true)
 |-- status: string (nullable = true)
 |-- subscription_term: string (nullable = true)
 |-- uid: string (nullable = true)
 |-- user_id: long (nullable = true)
 |-- ingestion_time: timestamp (nullable = false)
 |-- source_system: string (nullable = false)
 |-- user_name: string (nullable = false)
 |-- ingestion_type: string (nullable = false)
 |-- base_format: string (nullable = false)
 |-- file_size: integer (nullable = false)
 |-- rows_written: integer (nullable = false)
 |-- schema: string (nullable = false)
```
```sh
credit card
 |-- credit_card_expiry_date: string (nullable = true)
 |-- credit_card_number: string (nullable = true)
 |-- credit_card_type: string (nullable = true)
 |-- dt_current_timestamp: long (nullable = true)
 |-- id: long (nullable = true)
 |-- uid: string (nullable = true)
 |-- user_id: long (nullable = true)
 |-- ingestion_time: timestamp (nullable = false)
 |-- source_system: string (nullable = false)
 |-- user_name: string (nullable = false)
 |-- ingestion_type: string (nullable = false)
 |-- base_format: string (nullable = false)
 |-- file_size: integer (nullable = false)
 |-- rows_written: integer (nullable = false)
 |-- schema: string (nullable = false)
```
```sh
movies
 |-- adult: string (nullable = true)
 |-- belongs_to_collection: string (nullable = true)
 |-- dt_current_timestamp: long (nullable = true)
 |-- genres: string (nullable = true)
 |-- id: string (nullable = true)
 |-- imdb_id: string (nullable = true)
 |-- original_language: string (nullable = true)
 |-- original_title: string (nullable = true)
 |-- overview: string (nullable = true)
 |-- popularity: string (nullable = true)
 |-- production_companies: string (nullable = true)
 |-- production_countries: string (nullable = true)
 |-- release_date: string (nullable = true)
 |-- revenue: double (nullable = true)
 |-- status: string (nullable = true)
 |-- title: string (nullable = true)
 |-- user_id: long (nullable = true)
 |-- vote_average: double (nullable = true)
 |-- vote_count: double (nullable = true)
 |-- ingestion_time: timestamp (nullable = false)
 |-- source_system: string (nullable = false)
 |-- user_name: string (nullable = false)
 |-- ingestion_type: string (nullable = false)
 |-- base_format: string (nullable = false)
 |-- file_size: integer (nullable = false)
 |-- rows_written: integer (nullable = false)
 |-- schema: string (nullable = false)
```
 [A segunda etapa do pipeline](/images/spark/bronze_to_silver.py), consiste em tratar os dados de **`user`, `subscription`, `credit_card` e `movies`**, criando tabelas de dominio fazendo um join das tabelas **`users`**, **`subscription`** e **`credi card`** em uma nova tabela de dominio chamada ***`subcribers`***. Em adição, nesta etapa também foi criada uma outra tabela de dominio chamada ***`voters`***, que nada mais é a junção da tabela **`users`** e **`movies`**. Os dados de cada uma destas tabelas foram tratados e renomeados para atenderem ao proposito de uma tabela de dominio.

 Nesta etapa também foi adicionado a informação complementar **`processing_time`** em ambas as tabelas de dominio. Segue o schema das tabelas **`subscribers`** e **`voters`**, respectivamente:

 ```sh
 subscribers
 |-- user_id: long (nullable = true)
 |-- user_complete_name: string (nullable = false)
 |-- user_complete_address: string (nullable = false)
 |-- user_job: string (nullable = true)
 |-- user_ingestion_time: timestamp (nullable = true)
 |-- user_source_system: string (nullable = true)
 |-- user_user_name: string (nullable = true)
 |-- user_ingestion_type: string (nullable = true)
 |-- user_base_format: string (nullable = true)
 |-- user_file_size: integer (nullable = true)
 |-- user_rows_written: integer (nullable = true)
 |-- user_schema: string (nullable = true)
 |-- subscription_user_id: long (nullable = true)
 |-- subscription_plan: string (nullable = true)
 |-- subscription_price: decimal(4,2) (nullable = false)
 |-- subscription_status: string (nullable = true)
 |-- subscription_importance: string (nullable = true)
 |-- subscription_event_time: long (nullable = true)
 |-- credit_card_user_id: long (nullable = true)
 |-- credit_card_number: string (nullable = true)
 |-- credit_card_expiry_date: string (nullable = true)
 |-- credit_card_type: string (nullable = true)
 |-- credit_card_event_time: long (nullable = true)
 |-- credit_card_ingestion_time: timestamp (nullable = true)
 |-- credit_card_source_system: string (nullable = true)
 |-- credit_card_user_name: string (nullable = true)
 |-- credit_card_ingestion_type: string (nullable = true)
 |-- credit_card_base_format: string (nullable = true)
 |-- credit_card_file_size: integer (nullable = true)
 |-- credit_card_rows_written: integer (nullable = true)
 |-- credit_card_schema: string (nullable = true)
 |-- processing_time: timestamp (nullable = false)
 ```
 ```sh
voters
 |-- user_id: long (nullable = true)
 |-- user_complete_name: string (nullable = false)
 |-- user_complete_address: string (nullable = false)
 |-- user_job: string (nullable = true)
 |-- user_ingestion_time: timestamp (nullable = true)
 |-- user_source_system: string (nullable = true)
 |-- user_user_name: string (nullable = true)
 |-- user_ingestion_type: string (nullable = true)
 |-- user_base_format: string (nullable = true)
 |-- user_file_size: integer (nullable = true)
 |-- user_rows_written: integer (nullable = true)
 |-- user_schema: string (nullable = true)
 |-- movies_user_id: long (nullable = true)
 |-- movies_adult: string (nullable = true)
 |-- movies_title: string (nullable = true)
 |-- movies_popularity: double (nullable = true)
 |-- movies_vote_average: double (nullable = true)
 |-- movies_vote_count: double (nullable = true)
 |-- movies_release_date: string (nullable = true)
 |-- movies_genres_name: string (nullable = true)
 |-- movies_event_time: long (nullable = true)
 |-- movies_ingestion_time: timestamp (nullable = true)
 |-- movies_source_system: string (nullable = true)
 |-- movies_user_name: string (nullable = true)
 |-- movies_ingestion_type: string (nullable = true)
 |-- movies_base_format: string (nullable = true)
 |-- movies_file_size: integer (nullable = true)
 |-- movies_rows_written: integer (nullable = true)
 |-- movies_schema: string (nullable = true)
 |-- processing_time: timestamp (nullable = false)
 ```

 E por fim na [terceira etapa do pipeline](/images/spark/silver_to_gold.py), consiste basicamente em criar uma nova tabela na camada **`gold`** com as informações das tabelas de dominio da camada **`silver`**, com algumas colunas renomeadas mais alguns calculos simples, para servirem o proposito de entregar(servir) os dados destas tabelas tratadas para por exemplo um time de cientistas de dados. Nesta etapa foram criadas duas novas tabelas delta. As tabelas **`subers`** e **`voters`**, que correspondem as tabelas **`subscribers`** e **`voters`** da camada **`silver`**, respectivamente. Segue o schema de ambas as tabelas:

 ```sh
 subers
 |-- id: long (nullable = true)
 |-- name: string (nullable = true)
 |-- address: string (nullable = true)
 |-- plan: string (nullable = true)
 |-- importance: string (nullable = true)
 |-- status: string (nullable = true)
 |-- card: string (nullable = true)
 |-- time_to_process: long (nullable = true)
 |-- event_time: timestamp (nullable = false)
```
```sh
voters
 |-- id: long (nullable = true)
 |-- name: string (nullable = true)
 |-- title: string (nullable = true)
 |-- popularity: double (nullable = true)
 |-- average: double (nullable = true)
 |-- count: double (nullable = true)
 |-- release: string (nullable = true)
 |-- genre: string (nullable = true)
 |-- time_to_process: long (nullable = true)
 |-- event_time: timestamp (nullable = false)
 ```

<!--
kubectl apply -f dags/spark_jobs/delivery_data_from_silver_to_gold.yaml -n processing
kubectl logs -f transformation-and-enrichment-from-bronze-to-silver -n processing
kubectl delete sparkapplication delivery-data-from-silver-to-gold -n processing
 -->
## Estrutura de Arquivos

A estrutura de pastas está da seguinte maneira:

```bash
├── dags
├── images
│   ├── airflow
│   └── spark
├── manifests
│   ├── database
│   ├── deepstorage
│   ├── management
│   ├── misc
│   ├── monitoring
│   ├── orchestrator
│   └── processing
└── secrets
# 34 directories, 324 files
```

Serão explicados os arquivos e diretórios na seção de [Edição](#edição).

---
### Edição

Nesta seção haverão instruções caso você queira editar o projeto, explicando para que os diretórios são utilizados e também os arquivos de configuração.

- **[manifests](/manifests/)** - Diretório contendo todos os arquivos de aplicação do projeto, é criado um diretório `manifests` para que o código da aplicação possa ser isolado em um diretório e facilmente portado para outros projetos, se necessário;

  - **[database](/manifests/database/)** - Diretório para guardar os arquivos de configuração das aplicações de database, por exemplo, a configuração de instalação da aplicação `[postgres](/manifests/database/postgres.yaml)`;

to do o resto

<!-- CONTRIBUTING -->

## Contribuição

Contribuições são o que fazem a comunidade open source um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito apreciada**.

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/FeatureIncrivel`)
3. Adicione suas mudanças (`git add .`)
4. Comite suas mudanças (`git commit -m 'Adicionando uma Feature incrível!`)
5. Faça o Push da Branch (`git push origin feature/FeatureIncrivel`)
6. Abra um Pull Request

<!-- LICENSE -->

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

<!-- CONTACT -->

## Contato

GersonRS - [Github](https://github.com/gersonrs) - **gersonrodriguessantos8@gmail.com**
