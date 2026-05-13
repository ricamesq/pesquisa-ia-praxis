# Capítulo 1 — Por que isso importa

## 1.1 O problema da pesquisa fragmentada

Pesquisa acadêmica é uma das atividades humanas com mais alta densidade de informação por hora de trabalho. Um doutorando em educação lê facilmente 200 a 500 artigos em um ano de pesquisa preliminar. Um mestrando, entre 100 e 300. Um docente que orienta múltiplas teses, milhares ao longo da carreira.

Apesar disso, o **modo como armazenamos, organizamos e recuperamos esse material** mudou pouco nos últimos 25 anos. PDFs vão para a pasta Downloads. De lá, alguns sobem para uma pasta no Drive. Alguns mais importantes ganham nome melhorado e vão para subpastas temáticas — algumas vezes. Eventualmente, partes do material entram em um gerenciador de referências (EndNote, Zotero, Mendeley), com metadados parciais. Anotações ficam em margens de PDFs lidos, em cadernos físicos, em e-mails para si mesmo, em rascunhos de capítulos.

A consequência prática: **quando você precisa de um argumento, você lembra que leu, mas não acha**. Você sabe que viu uma discussão sobre algo em algum lugar, mas não localiza com rapidez. Quando precisa citar, refaz buscas. Quando quer comparar duas leituras, abre dois PDFs em paralelo e cansa.

A pesquisa fragmentada custa três coisas:

1. **Tempo** — horas perdidas em re-busca, re-leitura, re-fichamento.
2. **Profundidade** — você desiste de tentar fazer conexões cross-corpus porque o custo de descoberta é alto demais.
3. **Originalidade** — você cita o que lembra fácil, não o que seria mais relevante.

## 1.2 O que mudou (e ainda está mudando)

Quatro coisas mudaram silenciosamente nas últimas duas décadas:

### 1.2.1 Gerenciadores de referência viraram bancos de dados

O **Zotero** (criado em 2006) não é simplesmente uma "pasta de PDFs com metadados". Ele é um SQLite local que armazena ~30 campos por referência, suporta tags, coleções, anotações, e exporta para qualquer formato (RIS, BibTeX, CSL JSON, EndNote XML, PDF anotado). Tudo isso roda na sua máquina, fora da nuvem se você quiser.

A maioria dos usuários trata o Zotero como "um lugar pra pegar a citação no formato ABNT". Ele é um banco de dados de pesquisa pessoal completo.

### 1.2.2 Markdown virou padrão de notas científicas

O **Obsidian** (2020), junto com Logseq, RemNote, Roam Research e outros, popularizou o **vault Markdown** como sistema pessoal de gestão de conhecimento (PKM). A grande inovação: cada nota é um arquivo de texto plano (.md), legível pra sempre, versionável com Git, sincronizável por qualquer ferramenta de arquivo (OneDrive, Dropbox, Syncthing).

Plain-text radicalizou: você possui suas notas, em formato perpétuo, sem depender de servidor proprietário que pode fechar amanhã.

### 1.2.3 Bibliometria virou acessível

O **VOSviewer** (2010) reduziu a barreira para análise bibliométrica visual. Você importa um corpus de referências (RIS, CSV, Web of Science, Scopus), e o programa gera mapas de co-citação, co-autoria, co-ocorrência de palavras-chave, com clusters automáticos e overlay temporal.

Bibliometria virou uma ferramenta cotidiana de qualquer pesquisador, não mais coisa só de cientometristas profissionais.

### 1.2.4 IA agêntica chegou

Em 2023-2025, ferramentas como **Claude Code**, **Cursor**, **Aider** e similares amadureceram. Não são chatbots. São **orquestradores agênticos**: rodam comandos no terminal, leem arquivos, escrevem código, fazem refatorações, encadeiam ações.

O ponto crítico: para um orquestrador agêntico funcionar bem com pesquisa acadêmica, **precisa de uma estrutura subjacente** (vault Obsidian organizado, Zotero bem taggeado, scripts reproduzíveis). Sem estrutura, a IA produz lixo organizado. Com estrutura, produz amplificação real.

## 1.3 Letramento digital docente como direito

A literatura sobre **DigCompEdu** (Redecker, 2017) — referencial europeu de competências digitais para educadores — define seis áreas:

1. Engajamento profissional digital
2. Recursos digitais (acessar, criar, gerenciar)
3. Ensino e aprendizagem
4. Avaliação
5. Empoderamento dos aprendentes
6. Facilitação da competência digital dos aprendentes

Atravessam todas: **letramento informacional, comunicação digital, criação de conteúdo, segurança, resolução de problemas**.

A literatura brasileira mais recente (vide o corpus de 1.893 referências analisado em [`Cap. 5`](05-fluxo-integrado.md) deste livro) mostra que **a maioria dos docentes do ensino superior não tem domínio operacional dessas competências**. Quando se trata de gestão pessoal da própria pesquisa — não da pesquisa dos alunos — o gap é ainda maior.

Esse livro parte da hipótese de que **letramento digital docente é, em parte, letramento bibliométrico-computacional**: a capacidade de configurar e operar um ecossistema de ferramentas de pesquisa pessoal que respeite a integridade do pensamento e amplifique seu alcance.

Não é tecnocracia. É **autonomia epistêmica**.

## 1.4 O paradoxo da IA: poderosa mas insuficiente

Há uma tentação, em 2026, de "deixar a IA fazer". Pedir ao ChatGPT pra escrever a revisão de literatura. Mandar o Claude resumir 50 papers. Esperar que o Perplexity entregue argumento pronto.

**Não funciona — e por uma razão estrutural, não por preguiça da ferramenta.**

A IA generativa de hoje pode:
- ✅ Sintetizar texto que você já curou
- ✅ Reescrever em estilo formal
- ✅ Encontrar conexões em corpus organizado
- ✅ Gerar código pra automatizar tarefas estruturadas
- ✅ Conversar como interlocutor cético

A IA generativa de hoje NÃO pode:
- ❌ Decidir o que é importante na SUA pesquisa
- ❌ Substituir a leitura atenta dos textos centrais
- ❌ Manter consistência metodológica ao longo de meses
- ❌ Validar uma referência (verificar se realmente existe e diz o que diz)
- ❌ Reconhecer quando está alucinando

A diferença entre os dois grupos não é técnica. É **estrutural**: a IA funciona bem em cima de um corpus já curado por humano. Sem isso, ela funciona como um gerador de texto plausível mas vazio.

A integração que este livro propõe explora exatamente esse equilíbrio: você cura no Zotero (escolha, tagueia, organiza). A IA orquestra o resto (exporta, indexa, analisa, gera mapas). Você lê o que importa. A IA cuida da infraestrutura.

## 1.5 Por que escrever isso agora (e em português)

Tutoriais existentes sobre Obsidian + Zotero existem aos milhares em inglês. Sobre VOSviewer, há cursos pagos. Sobre Graphify, quase nada. Sobre IA agêntica para pesquisa acadêmica, quase tudo em inglês.

Três razões para este livro existir em português, agora:

1. **Letramento docente brasileiro precisa de material em vernáculo**. A literatura recente do nosso corpus (vide [`Cap. 6`](06-analises-possiveis.md)) mostra que termos em pt-BR sobre IA na educação chegam ~1 ano depois dos equivalentes em inglês, o que cria gap formativo concreto.

2. **A integração de cinco ferramentas é um nó técnico-pedagógico** que tem manuais isolados mas pouco material conectivo. Cada ferramenta tem seu manual; quase nenhum livro mostra o fluxo entre elas.

3. **Mestrado profissional precisa de produto técnico-pedagógico**. Se você é mestrando e está lendo, considere adaptar este livro para a sua área (saúde, direito, engenharia, ciências exatas) — a estrutura é reusável, o exemplo é só meu caso (educação + saúde digital).

## 1.6 O que NÃO está neste livro

Para evitar confusão, três temas explicitamente excluídos:

- **Análise estatística de textos científicos** (NLP profundo, embeddings, semantic search). Há boas literaturas sobre isso — começa-se em Spärck Jones, Salton, Manning. Aqui ficamos no nível da co-ocorrência de palavras-chave, que é mais transparente.
- **Plataformas como serviço** (Research Rabbit, Connected Papers, Elicit, Litmaps). São úteis, mas dependem de servidor proprietário. Este livro foca em ferramentas que você controla.
- **Recomendação personalizada de papers**. É outro campo (information retrieval) que não pertence à pesquisa pessoal.

## 1.7 O que está, e por que importa

Você vai sair deste livro sabendo:

- Configurar um vault Obsidian institucional sólido, com estrutura PARA e templates
- Conectar Zotero ao Obsidian via plugin **e** via scripts (caso o plugin quebre)
- Rodar Graphify para gerar um knowledge graph navegável do seu corpus
- Importar dados pro VOSviewer e gerar 3 mapas (network, density, overlay)
- Comparar dois snapshots do mesmo corpus para detectar shifts temáticos
- Cruzar múltiplos vaults sem misturar conteúdo (meta-grafo)
- Documentar tudo de forma reprodutível (Git, Markdown, scripts)

E o mais importante: você vai sair com **estrutura mental** para incorporar ferramentas novas conforme aparecerem, sem ter que reaprender o método.

---

> 📚 **Próximo capítulo:** [02 — Stack de ferramentas](02-stack-de-ferramentas.md)
