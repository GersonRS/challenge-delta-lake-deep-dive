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


O projeto visa solucionar o [desafio do workshop "Construindo seu próprio Data Lakehouse usando o Delta Lake"](https://github.com/GersonRS/ws-delta-lake-deep-dive/tree/main/challenge), que consiste em criar um pipeline de dados usando a arquitetura Medalion (Bronze, Silver e Gold), utilizando o Delta Lake.

O objetivo deste repositório é detalhar a criação de uma prova de conceito (POC) que soluciona o desafio, independentemente das tecnologias utilizadas. Ele visa criar um pipeline de dados que use a arquitetura Bronze, Silver e Gold, que possa ser utilizado como uma POC e um ponto de partida para projetos mais complexos, visto que o processo de criação e configuração de um pipeline de dados que segue essa arquitetura pode gerar complexidade e muitas vezes erros que atrasam o processo, atrapalhando o fluxo de desenvolvimento. A arquitetura em camadas é útil para garantir a qualidade dos dados e permitir que diferentes times possam acessar e usar dados em diferentes níveis de agregação.

# Fluxo de versionamento:
Projeto segue regras de versionamento [gitflow](https://www.atlassian.com/br/git/tutorials/comparing-workflows/gitflow-workflow).

# Feito Com

Abaixo segue o que foi utilizado na criação deste projeto:

- [Minikube](https://minikube.sigs.k8s.io/docs/start/) - Ferramenta de código aberto que permite criar um ambiente de teste do Kubernetes em sua máquina local. Com o Minikube, é possível criar e implantar aplicativos em um cluster Kubernetes em sua máquina local.
- [Helm](https://helm.sh/) - Ferramenta de gerenciamento de pacotes de código aberto para o Kubernetes. O Helm permite empacotar aplicativos Kubernetes em um formato padrão chamado de gráfico, que inclui todos os recursos necessários para implantar o aplicativo, incluindo configurações e dependências.
- [ArgoCD](https://argo-cd.readthedocs.io/en/stable/) - Ferramenta declarativa que usa a abordagem GitOps para implantar aplicações no Kubernetes. O Argo CD é gratuito, tem código aberto, é um projeto incubado pela CNCF, e possui uma interface web de visualização e gerenciamento dos recursos, mas também pode ser configurado via linha de comando.
- [Spark](https://spark.apache.org/) - O Spark é um framework de processamento de dados distribuído e de código aberto, que permite executar processamento de dados em larga escala, incluindo processamento em batch, streaming, SQL, machine learning e processamento de gráficos. Ele foi projetado para ser executado em clusters de computadores e fornece uma interface de programação fácil de usar para desenvolvedores;
- [Airflow](https://airflow.apache.org/) - O Airflow é uma plataforma de orquestração de fluxo de trabalho de dados de código aberto que permite criar, agendar e monitorar fluxos de trabalho complexos de processamento de dados. Ele usa uma linguagem de definição de fluxo de trabalho baseada em Python e possui uma ampla gama de conectores pré-construídos para trabalhar com diferentes sistemas de armazenamento de dados, bancos de dados e ferramentas de processamento de dados;
- [Reflector](https://github.com/emberstack/kubernetes-reflector) - O Reflector é uma ferramenta de sincronização de estado de código aberto que permite sincronizar recursos Kubernetes em diferentes clusters ou namespaces. Ele usa a abordagem de controlador de reconciliação para monitorar e atualizar automaticamente o estado dos recursos Kubernetes com base em um estado desejado especificado;
- [Minio](https://min.io/) - O Minio é um sistema de armazenamento de objetos de código aberto e de alta performance, compatível com a API Amazon S3. Ele é projetado para ser executado em clusters distribuídos e escaláveis e fornece recursos avançados de segurança e gerenciamento de dados;
- [Postgres](https://www.postgresql.org/) - O Postgres é um sistema de gerenciamento de banco de dados relacional de código aberto, conhecido por sua confiabilidade, escalabilidade e recursos avançados de segurança. Ele é compatível com SQL e é usado em uma ampla gama de aplicativos, desde pequenos sites até grandes empresas e organizações governamentais.

<!-- GETTING STARTED -->

# Começando

Este projeto contém uma solução de desafio que pode ser executada em um ambiente local ou em um ambiente em cloud. Para utilizar a solução, você precisará fazer um **`fork`** deste projeto e seguir os passos descritos abaixo.

## Pré-requisitos

Antes de prosseguir com a configuração e uso da solução, você precisará fazer um **`fork`** deste projeto e configurar um ambiente de desenvolvimento local para criar, testar e executar o projeto e ter uma chave ssh configurada em seu computador. Para isso, siga o guia abaixo:

### instalação do cluster

O primeiro passo é montar um ambiente com um cluster Kubernetes local para executar a aplicação e o pipeline de dados. Para esta POC, usaremos o cluster de Kubernetes **[minikube](https://minikube.sigs.k8s.io/docs/)**. [Siga este guia de instalação para instalar o Minikube](https://minikube.sigs.k8s.io/docs/start/).

Também usaremos o **[helm](https://helm.sh/)** para nos ajudar a instalar algumas aplicações. [Siga este guia de instalação para instalar o Helm](https://helm.sh/docs/intro/install/).

Após instalar esses pré-requisitos, é hora de iniciar o nosso cluster Minikube. Para que tudo ocorra bem, é aconselhável usar um cluster de no mínimo 8GB de memória e 2 CPUs. Execute o seguinte comando no terminal:

```
minikube start --memory=8000 --cpus=2
```

Para acessar alguns serviços via loadbalancer no Minikube, é necessário utilizar o [tunelamento do minikube](https://minikube.sigs.k8s.io/docs/handbook/accessing/#example-of-loadbalancer). Para isso, abra uma nova aba no seu terminal e execute o seguinte comando:
```sh
minikube tunnel
```

Com isso, o seu ambiente estará pronto para receber acessos via loadbalancer.

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

É hora de adicionar as ferramentas necessárias para o pipeline de dados. Para isso, é preciso criar secrets para armazenar senhas e informações confidenciais acessíveis pelas aplicações e processos do Spark. É necessário que eles estejam no namespace onde a aplicação está rodando e também no namespace processing, onde serão executados os processos do spark. Para realizar essa replicação dos secrets em diferentes namespaces, podemos usar o **[Reflactor](https://github.com/EmberStack/kubernetes-reflector)**, que evita a necessidade de recriar os secrets em namespaces diferentes. Para utilizá-lo, basta executar o comando a seguir:

Agora é hora de adicionar as outras ferramentas necesarias para o nosso pipeline de dados. E para isto precisamos criar `secrets` para armazenar senhas e informações censiveis, que  sejam acessiveis pelas aplicações e processos do **`Spark`**, por isso é necessario que eles estejam no namespace onde esta rodando a aplicação e também no namespace processing, onde será executado os processos do `spark`. Então para isto podemos usar o **[Reflactor](https://github.com/EmberStack/kubernetes-reflector)**, que ajudará a replicar os secrets nos namespaces necessários e a manter a segurança dos dados. Além disso, os comandos para instalar as configurações de acesso são importantes para garantir que apenas as pessoas autorizadas possam acessar os recursos do seu cluster, e para isto execute este comando:

```sh
kubectl apply -f manifests/management/reflector.yaml
```

> Antes de executar os comandos, você pode alterar os secrets dos arquivos localizados na pasta `secrets/` se quiser mudar as senhas de acesso aos bancos de dados e ao storage.

Após o Reflector estar funcionando, execute o comando que cria os secrets nos namespaces necessários:

```sh
# secrets
kubectl apply -f manifests/misc/secrets.yaml
```

> Caso não queira instalar o Reflactor para automatizar o processo de criar o secret em vários namespaces diferentes, você pode replicar manualmente o secret para outro namespace executando este comando:
`kubectl get secret minio-secrets -n deepstorage -o yaml | sed s/"namespace: deepstorage"/"namespace: processing"/| kubectl apply -n processing -f -`

Uma vez que os secrets estejam configurados, é possível instalar os bancos de dados e o storage do pipeline de dados com o seguinte comando:

```sh
# databases
kubectl apply -f manifests/database/postgres.yaml
# deep storage
kubectl apply -f manifests/deepstorage/minio.yaml
```

Por fim, instale o Spark e o Airflow, juntamente com suas permissões para executar os processos do Spark, executando os seguintes comandos:

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
<!-- Para criar um imagem do airflow com algumas libs inclusas, para isto execute o seguinte comando:
```sh 
eval $(minikube docker-env)
docker build -f images/airflow/dockerfile images/airflow/ -t airflow:0.1
``` -->

Antes de instalar o Airflow, é preciso atender a um requisito: criar um secret contendo sua `chave ssh`, para que o Airflow possa baixar as `DAGs` necessárias por meio do `gitSync`. É possível criar esse secret com o seguinte comando:

> Lembrando que você deve ter a `chave ssh` configurada em sua máquina.

```sh
kubectl create secret generic airflow-ssh-secret --from-file=gitSshKey=$HOME/.ssh/id_ed25519 -n orchestrator
```

```sh
# orchestrator
kubectl apply -f manifests/orchestrator/airflow.yaml
```

Em seguida, instale as configurações de acesso:

```sh
kubectl apply -f manifests/misc/access-control.yaml
```
Ótimo, agora que você configurou as ferramentas necessárias, temos o ambiente de desenvolvimento e de execução instalado e pronto para uso.

### Executando o projeto


Antes de tudo, é necessário possuir uma `imagem do Spark` que contenha todos os JARs necessários para a execução do nosso pipeline. Para criar uma imagem do Spark com essas especificações, execute:

```sh
eval $(minikube docker-env)
docker build --no-cache -f images/spark/dockerfile images/spark/ -t spark:0.1
```
Neste projeto, está sendo utilizada a versão 3.3.2 do Spark e a versão 2.2.0 do Delta, juntamente com todas as suas bibliotecas e JARs nas versões compatíveis, seguindo as compatibilidades do Delta [neste link](https://docs.delta.io/latest/releases.html) e neste link.

Após a imagem do Spark ser criada, abra a interface web do Airflow. Caso não saiba qual foi o IP atribuído ao webserver do Airflow, execute o seguinte comando para descobrir o IP:

```sh
kubectl get services -n orchestrator -l component=webserver,argocd.argoproj.io/instance=airflow -o jsonpath="{.items[0].status.loadBalancer.ingress[0].ip}"
```

Uma vez na interface do Airflow, ative o pipeline de dados `pipeline-delta-lake-deep-dive-complete` e veja a mágica acontecer. Ou, se preferir, você também pode executar cada etapa separadamente, seguindo a sequência:
  * `ingestion-from-local-data-file-to-bronze-tables`
  * `transformation-and-enrichment-from-bronze-to-silver`
  * `delivery-data-from-silver-to-gold`

Caso não deseje executar o pipeline pelo Airflow, você pode executar o pipeline de dados executando os seguintes comandos em sequência:
```sh
kubectl apply -f dags/spark_jobs/ingestion_from_local_data_file_to_bronze_tables.yaml -n processing
kubectl apply -f dags/spark_jobs/transform_and_enrichment_from_bronze_to_silver.yaml -n processing
kubectl apply -f dags/spark_jobs/delivery_data_from_silver_to_gold.yaml -n processing
```
Para verificar os arquivos no `data lakehouse`, acesse a interface web do `MinIO` e use as credenciais de acesso encontradas no arquivo *[minio-secrets.yaml](/secrets/minio-secrets.yaml)* na pasta *[secrets](/secrets/)*. Caso não saiba o IP atribuído ao MinIO, execute:

```sh
kubectl get services -n deepstorage -l app.kubernetes.io/name=minio -o jsonpath="{.items[0].status.loadBalancer.ingress[0].ip}"
```
Caso queira obter as credenciais de acesso do `MinIO`, execute:
```sh
echo "user: $(kubectl get secret minio-secrets -n deepstorage -o jsonpath="{.data.root-user}" | base64 -d)"
echo "password: $(kubectl get secret minio-secrets -n deepstorage -o jsonpath="{.data.root-password}" | base64 -d)"
```

## Pipeline Spark


O Pipeline Spark é um processo de três etapas que tem como objetivo criar uma camada de dados organizada e tratada para que possa ser utilizada por times de análise de dados. As etapas incluem a ingestão dos dados brutos (na camada Bronze), o tratamento e organização dos dados (na camada Silver) e a criação de uma tabela final que será utilizada pelos cientistas de dados (na camada Gold).

Para este desafio foi escolhida 4 conjunto de dados **(`user`, `subscription`, `credit_card` e `movies`)**.
Os codigos spark foram escritos em `python` ***(Pyspark)*** e adicionados a uma [imagem docker](images/spark/dockerfile). Optei colocar todos os meus códigos spark na mesma `imagem`, pela simplicidade de desenvolver e explicar. Apesar de que este pode não ser a melhor pratica para esse tipo de problema(mas funciona).

Os dados da **`landing`** disponibilizados pelo desafio, também foram incluidos na `imagem`, os quais são transformados em **tabelas `delta`** em um `lakehouse` criado no `minio`. Sei que esta não foi a melhor pratica, mas esta também foi uma escolha pela simplicidade de replicação do projeto *(e minha falta de tempo de colocar no bucket)*.

### Carregando os dados na **`Bronze`**

[Na primeira etapa do pipeline](/images/spark/ingestion_to_bronze.py), os dados brutos são carregados da pasta landing (que estão na [imagem](/images/spark/dockerfile)) e transformados em tabelas Delta no lakehouse, criado no Minio. A criação de tabelas Delta facilita o gerenciamento dos dados, permitindo que novos dados possam ser adicionados e atualizados posteriormente. Também são adicionadas informações adicionais como ingestion_time e file_size, que podem ser úteis para análises posteriores. É possivel ver todos as informações adicionais nas linhas `56-63` do arquivo [ingestion_to_bronze.py](/images/spark/ingestion_to_bronze.py).

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
[Na segunda etapa](/images/spark/bronze_to_silver.py), os dados de diferentes fontes, como **`user`**, **`subscription`**, **`credit_card`** e **`movies`**, são tratados e organizados em tabelas de `domínio`. Nesta etapa, tabelas de `domínio` como **`subscribers`** e **`voters`** são criadas, que são basicamente junções de diferentes tabelas de fontes. Os dados são tratados e renomeados para que sejam mais úteis para análises futuras.

Nesta etapa também foi adicionado a informação complementar **`processing_time`** em ambas as tabelas de `domínio`. Segue o schema das tabelas **`subscribers`** e **`voters`**, respectivamente:

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
[Na terceira etapa do pipeline](/images/spark/silver_to_gold.py), uma nova tabela é criada na camada **`Gold`**, com as informações tratadas das tabelas de `domínio` da camada **`Silver`**. As tabelas **`subscribers`** e **`voters`** são renomeadas como **`subers`** e **`voters`**, respectivamente, e novas `colunas` e cálculos são adicionados para que sejam úteis para análises futuras. Por fim, as tabelas resultantes são entregues aos cientistas de dados para que possam ser utilizadas em análises mais aprofundadas. Segue o schema de ambas as tabelas:

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

Certifique-se de testar e validar seus pipelines de dados antes de implantá-los em produção. Isso ajudará a garantir que seus processos estejam funcionando corretamente e que os dados estejam sendo tratados de maneira apropriada.
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
