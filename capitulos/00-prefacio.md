# Prefácio

> *"Não tem como pensar bem com a cabeça desorganizada. Não tem como ter cabeça organizada quando a pesquisa está em 14 pastas no Drive, 3 caixas no Gmail e um caderno físico que não cabe na mochila. Este livro é sobre fechar essa fragmentação — não fazendo virar plataforma única, mas conectando o que já está aí com fios que você consegue ver."*

## Por que escrevi isso

Em 12 de maio de 2026, em uma sessão de oito horas com o Claude Code, fiz algo que vinha adiando há dois anos: integrei minha biblioteca de 1.893 referências do Zotero ao meu Obsidian, indexei tudo como grafo navegável, comparei com meus mapas bibliométricos antigos do VOSviewer, e descobri — pela diferença entre antes e depois — que o foco da minha dissertação tinha se deslocado sem que eu percebesse conscientemente.

A descoberta não veio da ferramenta. Veio do **diálogo entre as ferramentas**.

Esse livrinho é a documentação reprodutível do método. Não é tutorial de produto (existem milhares). É a tentativa de mostrar que o que move pesquisa séria é **estrutura paciente**, não busca rápida. E que ferramentas digitais podem servir essa paciência, em vez de competir com ela.

## Quem deveria ler isto

Quem está em algum desses lugares:

- Tem mais de 500 referências e perdeu o controle do corpus
- Já usa Zotero mas não tira proveito dele além de gerar citações
- Tentou Obsidian e desistiu porque "não sabia o que pôr lá"
- Acha que IA vai "fazer a tese" — vai descobrir aqui que não
- Acha que IA "não tem nada a oferecer pra pesquisa séria" — vai descobrir aqui que tem, mas só se você der ela uma estrutura pra orquestrar
- Quer um produto técnico-pedagógico para mestrado profissional que tenha utilidade real
- Trabalha com bibliotecas universitárias e quer entender o estado da arte em pesquisa pessoal computacional

## Quem NÃO deveria ler isto

- Quem quer que a IA escreva a tese (não vai escrever; e este livro vai te frustrar)
- Quem busca solução "no-code, point and click" pra pesquisa (tem alguns scripts Python aqui, prepare-se)
- Quem rejeita por princípio o uso de software proprietário (Zotero é open-source, Obsidian é freeware, mas Claude Code não é — substitua por outro CLI agêntico se preferir)

## Convenções deste livro

- **Comandos de terminal** aparecem em blocos como este:
  ```bash
  python scripts/export_zotero_to_vault.py
  ```
- **Caminhos de arquivos** aparecem em `caminho/arquivo.md`
- **Citações de tags ou termos técnicos** vão em `texto monoespaçado`
- **Recomendações fortes** começam com 🎯
- **Armadilhas conhecidas** começam com ⚠️
- **Boxes de prática** começam com 🧰

## Como o livro foi escrito

Este livro foi escrito **junto com o Claude Code** em uma sessão única. A estrutura é minha. Os exemplos são da minha pesquisa real (mestrado em Ciências e Matemática na Universidade Cruzeiro do Sul, 2026). O texto é uma colaboração: eu escolhi o que dizer, o Claude ajudou a organizar e parafrasear. Cada script Python é funcional e foi rodado contra minha base real antes de entrar aqui.

Não é livro IA-gerado. É livro IA-mediado — diferença que vai ficar mais clara conforme você ler.

## Estrutura

1. **Por que isso importa** — o contexto, o problema, o letramento docente como direito
2. **Stack de ferramentas** — Zotero, Obsidian, Graphify, VOSviewer, Claude Code
3. **Setup** — uma vez e nunca mais
4. **Fluxo integrado** — o coração do livro: o passo a passo real
5. **Análises possíveis** — o que esse fluxo permite que você não conseguia antes
6. **Armadilhas aprendidas** — coisas que custaram horas
7. **Como replicar** — checklist do zero
8. **Anexo** — catálogo de ferramentas auxiliares (Graphify, ECC, scripts comentados)
9. **Referências** — bibliografia comentada

Não precisa ler em ordem. Cada capítulo se vira sozinho.

---

> 📚 **Próximo capítulo:** [01 — Por que isso importa](01-por-que-isso-importa.md)
