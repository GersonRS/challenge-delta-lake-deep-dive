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
- [Começando](#come%C3%A7ando)
  - [Pré-requisitos](#pr%C3%A9-requisitos)
  - [Estrutura de Arquivos](#estrutura-de-arquivos)
  - [Instalação](#instala%C3%A7%C3%A3o)
    - [Passo Adicional no Android](#passo-adicional-no-android)
  - [Edição](#edi%C3%A7%C3%A3o)
  - [Publicação](#publica%C3%A7%C3%A3o)
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

### instalação e configuração de um ambiente local

Primeiramente precisamos montar um ambiente com um cluster kubernetes para que possamos executar nossa aplicação e execução do pipeline de dados.

Para esta POC usaremos o cluster de kubernetes **[minikube](https://minikube.sigs.k8s.io/docs/)**. Para instalar o minikube basta seguir [este guia de instalação](https://minikube.sigs.k8s.io/docs/start/).

Também usaremos o **[helm](https://helm.sh/)** para nos auxiliar na instalação de algumas aplicações. Para instalar o helm [siga este guia](https://helm.sh/docs/intro/install/).

Após estes dois pre-requisitos instalados é hora de iniciar o nosso cluster minikube:
```
minikube start --memory=8000 --cpus=2
```
> para que ocorra tudo bem é aconselhavel usar um cluster de no minimo 8Gb e 2 CPUs

### Instalação do ferramental

Depois do ambiente inicializado será necessario instalar algumas aplicações que serão responsaveis por manter e gerenciar nosso pipeline de dados.

Estando conectado em um cluster Kubernetes, execute os seguintes comandos:

```sh
kubectl create namespace orchestrator
kubectl create namespace database
kubectl create namespace ingestion
kubectl create namespace processing
kubectl create namespace datastore
kubectl create namespace deepstorage
kubectl create namespace cicd
kubectl create namespace app

helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm install argocd argo/argo-cd --namespace cicd --version 5.27.1
```

> Para que alguns serviços sejam acessiveis via loadbalancer no minikube, é necessario que você use o [tunelamento do minikube](https://minikube.sigs.k8s.io/docs/handbook/accessing/#example-of-loadbalancer).
> Para isto abra uma nova aba do seu terminal e digite o seguinte commando:
>
>`minikube tunnel`
>
> Com isto o seu ambiente esta pronto para receber acessos via loadbalancer

Uma vez habilitado o LoadBalancer, altere service do argo para loadbalancer:
```sh
# create a load balancer
kubectl patch svc argocd-server -n cicd -p '{"spec": {"type": "LoadBalancer"}}'
```

Em seguida mude para o namespace da instalação do argo:

```sh
kubens cicd
```
Depois veja o ip atribiudo para acessar o argo e o seu respectivo password:
```sh
# retrieve load balancer ip
kubectl get services -n cicd -l app.kubernetes.io/name=argocd-server,app.kubernetes.io/instance=argocd -o jsonpath="{.items[0].status.loadBalancer.ingress[0].ip}"

# get password to log into argocd portal
kubectl get secret argocd-initial-admin-secret -n cicd -o jsonpath="{.data.password}" | base64 -d
```

Uma vez em posse destas informações, acesse a interface web do argo e adicione o seu repositorio no argo.

Agora é hora de adicionar as outras ferramentas necesarias para o nosso pipeline de dados. Começando com os databases e storage do nosso pipeline de dados, execute os seguintes comandos:

> Antes de executar os comando você pode alterar os secrets dos arquivos localizados na pasta `secrets/` , caso queira mudar os passwords de acessos aos databases e storage

```sh
# secrets
kubectl apply -f secrets/postgres-secrets.yaml
kubectl apply -f secrets/minio-secrets.yaml
# databases
kubectl apply -f app-manifests/database/postgres.yaml
# deep storage
kubectl apply -f app-manifests/deepstorage/minio.yaml
```

E por fim instale o Spark e o Airflow, executando os seguintes comandos:

> Antes de instalar o airflow lembre-se de alterar o **`gitSshKey`** na linha `47` do arquivo `app-manifests/orchestrator/airflow.yaml` para a chave privada do seu ssh conectado com o github

```sh
# add & update helm list repos
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm repo add apache-airflow https://airflow.apache.org/
helm repo update
```

```sh
# processing
kubectl apply -f app-manifests/processing/spark.yaml
```
```sh
# orchestrator
kubectl apply -f app-manifests/orchestrator/airflow.yaml
```

```sh
eval $(minikube docker-env)
docker build -f images/airflow/dockerfile images/airflow/ -t gersonrs/airflow:0.1
```





## Estrutura de Arquivos

A estrutura de arquivos está da seguinte maneira:

```bash

```

Serão explicados os arquivos e diretórios na seção de [Edição](#edição).

---
### Edição

Nesta seção haverão instruções caso você queira editar o template, explicando para que os diretórios são utilizados e também os arquivos de configuração.

- **src** - Diretório contendo todos os arquivos da aplicação, é criado um diretório `src` para que o código da aplicação possa ser isolado em um diretório e facilmente portado para outros projetos, se necessário;

  - **config** - Diretório para guardar os arquivos de configuração da aplicação, por exemplo, a configuração de uso do Reactotron e configuração de inicialização do Firebase;

    - **ReactotronConfig.js** - Arquivo contendo a configuração do Reactotron, com os Plugins `reactotron-redux` e `reactotron-redux-saga`, para ser usado na aplicação;

  - **images** - Diretório para armazenar imagens em geral que possam ser utilizadas na aplicação, esse diretório pode ser renomeado para `assets` e dentro de `assets` criar um novo diretório para guardar somente as imagens, assim é possível ter um diretório para guardar todo tipo de arquivo, e não apenas imagens;

  - **pages** - Diretório onde ficam as páginas (telas) da aplicação, como forma de padronização e boas práticas toda página fica dentro de um diretório com seu nome;

    - **Main** - Diretório exemplo de uma página cujo nome é **Main**, por padrão foi adotado usar sempre como nome do diretório o nome da página em camelCase, dentro desse diretório é necessária a criação ao menos do arquivo `index.js`;

      - **index.js** - Arquivo com toda a lógica da página, com os componentes visuais a serem renderizados e também o código para conectar o componente ao Redux para acessar o State global e as Actions criadas nos Ducks;

  - **services** - Diretório onde serão criados os arquivos relacionados a serviços utilizados na aplicação, por exemplo, requisições HTTP, autenticação com Firebase ou qualquer outro serviço que for utilizado;

    - **api.js** - Arquivo com a configuração da biblioteca Axios para envio de requisições HTTP, o endereço que vem configurado por padrão é para a API do Github;

  - **store** - Diretório onde será criada toda a estrutura do Redux para a aplicação, como os **Ducks** (Reducers + Action Types + Action Creators), os **Sagas** e um arquivo para centralizar toda essa configuração e disponibilizar para o restante da aplicação;

    - **ducks** - Diretório destinado a centralizar os **Ducks** da aplicação para padronização na estrutura relacionada ao Redux;

      - **index.js** - Arquivo responsável por importar cada **Duck** criado e combiná-los em um só para serem usados no Redux através da função `combineReducers()`;

    - **sagas** - Diretório destinado a centralizar os **Sagas** da aplicação para padronização na estrutura relacionada ao Redux;

      - **index.js** - Arquivo responsável por relacionar as **Actions** disparadas pela aplicação às funções do **Saga**, que são Funções Generator, nele é definido os **Action Types** a serem "escutados" e qual função executar quando um Action Creator for executado;

    - **index.js** - Arquivo responsável por executar a configuração para o funcinamento do Redux + Redux Saga, dentre suas funções estão: criar um **Middleware** para monitorar as Actions disparadas na aplicação, aplicar o middleware criado juntamente com um Enhancer que monitora o fluxo de uma função do **Saga**, criar o store global da aplicação combinando os reducers existentes e exportar o state criado;

  - **index.js** - Arquivo responsável por centralizar o código do diretório `src`, nele é inserido o HOC Provider do `react-redux` que é o responsável por disponilizar o state global para a aplicação, e dentro do Provider são chamadas as rotas tal como qualquer outra configuração que precise ser executada na inicialização da aplicação, ele é como um _Entry Point_ do diretório `src`;

  - **routes.js** - Arquivo com as configurações de navegação da aplicação, nele são criados os Navigators disponibilizados na biblioteca React Navigation;

- **.editorconfig** - Arquivo destinado à configuração do plugin Editor Config, que padroniza algumas configurações para o editor em diferentes ambientes;

- **.eslintrc.json** - Arquivo de configuração do ESLint, é nele que são inseridas as regras e configurações de Linting do projeto, tal como a configuração do Resolver para o Babel Plugin Root Import e configuração da variável global `__DEV__`;

- **babel.config.js** - Arquivo de configuração do Babel, é nele que é configurado o Babel Plugin Root Import para aceitar imports absolutos na aplicação usando o diretório `src` como raiz;

- **dependencies.json** - Arquivo contendo apenas um objeto com a lista de dependências que devem ser instaladas na aplicação, vale lembrar que as dependências que já vem por padrão no projeto como `react` e `react-native` não precisam estar nessa lista, a menos que você queira gerenciar a versão dessas libs;

- **devDependencies.json** - Arquivo contendo apenas um objeto com a lista de dependências de desenvolvimento que devem ser instaladas na aplicação, vale lembrar que as dependências de desenvolvimento que já vem por padrão no projeto como `@babel/core`, `@babel/runtime`, entre outras, não precisam estar nessa lista, a menos que você queira gerenciar a versão dessas libs;

- **index.js** - Arquivo raiz da aplicação, também chamado de _Entry Point_, é o primeiro arquivo chamado no momento do build e execução da aplicação, nele é chamado o arquivo `src/index.js` que por sua vez chama as rotas da aplicação;

- **jsconfig.json** - Arquivo de configuração do JavaScript no Editor, ele é o responsável por ativar o Auto Complete de códigos JavaScript na aplicação;

- **package.json** - Diferente dos projetos comuns, esse arquivo tem as configurações necessárias para a publicação do Template no NPM, para saber mais sobre isso veja a seção abaixo.

<!-- CONTRIBUTING -->

## Contribuição

Contribuições são o que fazem a comunidade open source um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito apreciada**.

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/FeatureIncrivel`)
3. Adicione suas mudanças (`git add .`)
4. Comite suas mudanças (`git commit -m 'Adicionando uma Feature incrível!`)
5. Faça o Push da Branch (`git push origin feature/FeatureIncrivel`)
6. Abra um Pull Request

Para testar o template de um caminho local, coloque o caminho absoluto junto com o prefixo `file://`
```
react-native init AwesomeContribution --template file:///Users/Dev/contributions/react-native-template-rocketseat-advanced
```

<!-- LICENSE -->

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

<!-- CONTACT -->

## Contato

Rocketseat - [Github](https://github.com/rocketseat) - **oi@rocketseat.com.br**
