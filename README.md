# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Técnicas Aplicadas (Fase 2)

### Objetivo
O objetivo desta fase foi otimizar o prompt responsável por converter relatos de bugs em User Stories, buscando melhorar seu desempenho nas métricas de avaliação do LangSmith:

- Helpfulness
- Correctness
- F1-Score
- Clarity
- Precision


### Técnicas Utilizadas

#### 1. Few-shot Learning

##### Justificativa

O prompt original não apresentava exemplos de entrada e saída.

Foram adicionados exemplos completos para ensinar ao modelo:

- Estrutura da resposta
- Nível de detalhamento esperado
- Escrita de critérios de aceitação
- Identificação de edge cases

##### Aplicação Prática

Foram criados três exemplos representando diferentes cenários de negócio:

- Isolamento de dados entre tenants (Multi-Tenant)
- Renovação de autenticação utilizando Refresh Token
- Exportação de relatórios PDF

##### Exemplo Multi-Tenant

Entrada:

```text
Usuários da empresa Alpha estão visualizando registros pertencentes à empresa Beta ao acessar a tela de pedidos.
```

Saída:

```markdown
## User Story

Como usuário de uma empresa cadastrada na plataforma,
Quero visualizar apenas os dados pertencentes ao meu tenant,
Para garantir a confidencialidade e integridade das informações da minha organização.
```

##### Métricas Impactadas

- Correctness
- Precision
- F1-Score

---

#### 2. Role Prompting

##### Justificativa

O prompt original utilizava apenas a persona "Você é um assistente", o que deixava a resposta muito aberta.

Foi definida uma persona especializada em Product Management e metodologias ágeis para direcionar o modelo a produzir User Stories alinhadas às boas práticas de Scrum.

##### Aplicação Prática

Foi utilizada a seguinte persona:

```text
Você é um Product Manager Sênior especializado em:

- Scrum
- Agile
- Product Discovery
- Product Delivery
- Refinamento de Backlog
- Escrita de User Stories
```

##### Benefícios Esperados

- Melhor contextualização do problema
- User Stories mais alinhadas com práticas ágeis
- Critérios de aceitação mais relevantes
- Menor probabilidade de respostas genéricas

##### Métricas Impactadas

- Helpfulness
- Correctness

---

#### 3. Skeleton of Thought

##### Justificativa

Para reduzir a variabilidade das respostas, foi definido um esqueleto obrigatório.

Essa estrutura garante que todas as respostas possuam as mesmas seções e facilita tanto a leitura quanto a avaliação automática.

##### Aplicação Prática

```markdown
## Resumo do Problema

## User Story

Como...
Quero...
Para...

## Critérios de Aceitação

- ...

## Edge Cases

- ...
```

##### Benefícios Esperados

- Melhor organização da resposta
- Facilidade de leitura
- Saídas mais previsíveis
- Menor risco de omissão de informações importantes

##### Métricas Impactadas

- Clarity
- Precision
- F1-Score

### Métricas

| Métrica | Objetivo | Exemplo |
|----------|----------|----------|
| **Helpfulness** | Avalia se a resposta é útil para resolver o problema. | User Story clara e acionável para o time de desenvolvimento. |
| **Correctness** | Verifica se a User Story representa corretamente o bug informado. | Bug sobre autenticação gera uma User Story relacionada à autenticação. |
| **F1-Score** | Mede a similaridade entre a resposta gerada e a resposta esperada. | Quanto mais próxima da referência, maior a pontuação. |
| **Clarity** | Avalia organização e facilidade de leitura. | Resposta estruturada com seções bem definidas. |
| **Precision** | Mede o foco da resposta no problema informado. | Evita incluir funcionalidades ou informações não relacionadas ao bug. |

### Relação entre Técnicas e Métricas

| Técnica | Helpfulness | Correctness | Clarity | Precision | F1-Score |
|----------|:----------:|:----------:|:--------:|:---------:|:--------:|
| Few-shot Learning | | ✓ | | ✓ | ✓ |
| Role Prompting | ✓ | ✓ | | | |
| Skeleton of Thought | | | ✓ | ✓ | ✓ |

### Resultado Esperado

A combinação das técnicas foi escolhida para melhorar simultaneamente as cinco métricas avaliadas pelo LangSmith.

| Técnica | Principal contribuição |
|----------|------------------------|
| **Few-shot Learning** | Ensina o formato esperado da resposta e aumenta a consistência. |
| **Role Prompting** | Direciona o modelo para responder como um Product Manager experiente. |
| **Skeleton of Thought** | Padroniza a estrutura da resposta e reduz variações entre execuções. |

Espera-se, com essa combinação, atingir pontuação **igual ou superior a 0,8** em todas as métricas de avaliação (Helpfulness, Correctness, F1-Score, Clarity e Precision).

## Resultados Finais
### LangSmith
#### Dashboard
![evaluate-1](/docs/langsmith-dashboard.png)

[Link para o Dashboard](https://smith.langchain.com/o/b24bdd88-0126-4580-8f00-4e081631a24f/projects/p/841ed629-ab5e-4d33-94bb-aa57130c0fe9?timeModel=%7B%7D&custom_run_filter_view_id=6e33c201-6332-4c1b-a23f-f240ea3d9fc4&runview=traces&searchModel=%7B%22filter%22%3A%22eq%28is_root%2C+true%29%22%2C%22traceFilter%22%3A%22%22%2C%22treeFilter%22%3A%22%22%7D) (não foi encontrada a opção para tornar o dashboard público)

#### Dataset
![evaluate-1](/docs/langsmith-dataset.png)

### Terminal output
```
==================================================
AVALIAÇÃO DE PROMPTS OTIMIZADOS
==================================================

Provider: openai
Modelo Principal: gpt-4.1-mini
Modelo de Avaliação: gpt-4.1-mini

Criando dataset de avaliação: mba-fc-eval...
   ✓ Carregados 15 exemplos do arquivo datasets/bug_to_user_story.jsonl
   ✓ Dataset 'mba-fc-eval' já existe, usando existente

======================================================================
PROMPTS PARA AVALIAR
======================================================================

Este script irá puxar prompts do LangSmith Hub.
Certifique-se de ter feito push dos prompts antes de avaliar:
  python src/push_prompts.py


🔍 Avaliando: egon89/bug_to_user_story_v2
   Puxando prompt do LangSmith Hub: egon89/bug_to_user_story_v2
   ✓ Prompt carregado com sucesso
   Dataset: 15 exemplos
   Avaliando exemplos...
      [1/15] F1:0.87 Clarity:0.90 Precision:0.95
      [2/15] F1:0.87 Clarity:0.85 Precision:0.95
      [3/15] F1:0.87 Clarity:0.95 Precision:1.00
      [4/15] F1:0.69 Clarity:0.80 Precision:0.90
      [5/15] F1:0.80 Clarity:0.85 Precision:0.90
      [6/15] F1:1.00 Clarity:0.85 Precision:1.00
      [7/15] F1:0.90 Clarity:0.85 Precision:0.90
      [8/15] F1:0.87 Clarity:0.90 Precision:1.00
      [9/15] F1:0.85 Clarity:0.80 Precision:0.80
      [10/15] F1:0.90 Clarity:0.85 Precision:0.90
      [11/15] F1:0.85 Clarity:0.80 Precision:0.90
      [12/15] F1:0.90 Clarity:0.85 Precision:1.00
      [13/15] F1:0.95 Clarity:0.90 Precision:1.00
      [14/15] F1:0.85 Clarity:0.85 Precision:1.00
      [15/15] F1:0.85 Clarity:0.85 Precision:0.90

==================================================
Prompt: egon89/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.90 ✓
  - Correctness: 0.90 ✓

Métricas Base:
  - F1-Score: 0.87 ✓
  - Clarity: 0.86 ✓
  - Precision: 0.94 ✓

--------------------------------------------------
📊 MÉDIA GERAL: 0.8933
--------------------------------------------------

✅ STATUS: APROVADO - Todas as métricas >= 0.8

==================================================
RESUMO FINAL
==================================================

Prompts avaliados: 1
Aprovados: 1
Reprovados: 0

✅ Todos os prompts atingiram todas as métricas >= 0.8!
```

![evaluate-1](/docs/evaluate-1.png)
![evaluate-2](/docs/evaluate-2.png)

### Evolução do Prompt (v1 → v2)

A primeira versão do prompt possuía apenas uma instrução genérica para transformar um relato de bug em uma User Story.

```text
Você é um assistente que ajuda a transformar relatos de bugs de usuários em tarefas para desenvolvedores.

Analise o relato de bug abaixo e crie uma user story a partir dele.
```

Essa abordagem apresentava algumas limitações:

- Não definia uma persona especializada.
- Não estabelecia um formato obrigatório de resposta.
- Não possuía exemplos de entrada e saída.
- Não orientava como lidar com ambiguidades.
- Produzia respostas inconsistentes entre diferentes execuções.

A versão **v2** foi reformulada utilizando técnicas de Prompt Engineering para tornar as respostas mais consistentes e previsíveis.

| Aspecto | v1 | v2 |
|---------|----|----|
| Persona | Assistente genérico | Product Manager Sênior |
| Estrutura da resposta | Livre | Formato obrigatório |
| Few-shot Learning | Não | Sim (3 exemplos) |
| Critérios de Aceitação | Não definido | Obrigatório |
| Edge Cases | Não | Obrigatório |
| Regras de comportamento | Poucas | Explícitas |
| Consistência das respostas | Baixa | Alta |


#### Tabela comparativa
| Métrica | v1 (prompt ruim) | v2 (otimizado) | Aprovado? |
|---------|-----------------|----------------|-----------|
| Helpfulness | 0.45 | 0.90 | ✅ |
| Correctness | 0.52 | 0.90 | ✅ |
| F1-Score | 0.48 | 0.87 | ✅ |
| Clarity | 0.50 | 0.86 | ✅ |
| Precision | 0.46 | 0.94 | ✅ |

### Tracing detalhado

- [Tracing *carrinho está inoperante*](docs/tracing/tracing-e7df68f2-c586-4d05-aaf3-aafffbba1ea0.json)
  - [Tracing *calcular precision e recall*](docs/tracing/tracing-e7df68f2-c586-4d05-aaf3-aafffbba1ea0-child-3acd0596-2371-4c46-a1d8-d60b6e9bf27b.json)
  - [Tracing *medição de clareza*](docs/tracing/tracing-e7df68f2-c586-4d05-aaf3-aafffbba1ea0-child-bf3f1994-4c5b-4168-9a73-3ec98dfaba97.json)
- [Tracing *relatórios gerenciais*](docs/tracing/tracing-95d28c05-cc38-470f-af8d-5c805f118ea1.json)
- [Tracing *compra de produto fora de estoque*](docs/tracing/tracing-77da31bf-71f1-4cda-92d9-d6c789a4eb4f.json)
- [Tracing *sistema de checkout com múltiplas falhas críticas*](docs/tracing/tracing-8a22e1d9-332d-481b-9425-0c0eb8ec0784.json)

## Como Executar

Realize uma cópia do arquivo `.env.example` para `.env` (`cp .env.example .env`) e configure as variáveis de ambiente necessárias. Foi utilizado o modelo `gpt-4.1-mini` da OpenAI para avaliação, mas você pode alterar para outro modelo compatível com LangSmith.

```sh
# Inicie o container:
docker compose up -d --build

# Acesse o container:
docker compose exec python_app bash

# Execute os scripts dentro do container, por exemplo:
python src/pull_prompts.py
```

### Fases
- Fase 1 (*Pull do prompt inicial do LangSmith*): `python src/pull_prompts.py`
- Fase 2 (*Refatoração do prompt com técnicas avançadas de Prompt Engineering*): editar o arquivo `prompts/bug_to_user_story_v2.yml`
- Fase 3 (*Push do prompt otimizado para o LangSmith*): `python src/push_prompts.py`
- Fase 4 (*Avaliação do prompt otimizado*): `python src/evaluate.py`
- Fase 5 (*Verificação de testes*): `pytest -v tests/test_prompts.py`
