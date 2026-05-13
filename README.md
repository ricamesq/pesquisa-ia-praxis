# Pesquisa IA Práxis
### Um manual prático de letramento bibliométrico-computacional para pesquisadores em educação e saúde

> Versão 0.1 · maio/2026 · Ricardo Mesquita · Licença CC BY-SA 4.0

---

## O que é este livrinho

Um guia passo a passo, em português, de como integrar **cinco ferramentas** que isoladamente são úteis, mas juntas viram um sistema de pesquisa acadêmica que respeita a inteligência humana e amplifica seu alcance:

| Ferramenta | Função no fluxo |
|---|---|
| **Zotero** | Banco de dados pessoal de referências bibliográficas |
| **Obsidian** | Cérebro de trabalho — notas, fichamentos, escrita |
| **Graphify** | Extração de conhecimento estruturado em grafo |
| **VOSviewer** | Mapas bibliométricos visuais |
| **Claude Code** | Orquestrador agêntico que cose tudo |

A integração não é um truque técnico — é uma **postura epistemológica**: tratar a pesquisa como construção paciente de um corpus que dialoga consigo mesmo, em vez de busca apressada por informação.

## Para quem este livrinho serve

- Mestrandos e doutorandos em qualquer área das ciências humanas e da saúde
- Docentes universitários que querem reorganizar seu corpus de pesquisa
- Pesquisadores em educação investigando letramento digital docente
- Bibliotecários e gestores de informação interessados em métodos reprodutíveis
- Qualquer pessoa que sinta que sua pesquisa virou pilhas de PDFs perdidos no Drive

## O que você vai aprender

1. Por que pesquisa fragmentada empobrece pensamento (e como recompor)
2. Como configurar cada ferramenta uma vez e nunca mais lutar com configuração
3. Como exportar 1.893 referências do Zotero para 1.893 notas Markdown em 15 segundos
4. Como indexar seu vault como grafo de conhecimento navegável
5. Como gerar mapas bibliométricos (network, density, overlay temporal)
6. Como detectar deslocamentos temáticos no seu corpus ao longo dos anos
7. Como cruzar múltiplos vaults sem misturar conteúdo
8. Como evitar 10 armadilhas que custaram horas de retrabalho

## Como ler este livrinho

| Se você é | Leia primeiro |
|---|---|
| Iniciante em pesquisa | Cap. 1 (motivação) → Cap. 3 (setup) → Cap. 4 (fluxo) |
| Já usa Zotero, quer integrar Obsidian | Cap. 2 (stack) → Cap. 4 (fluxo) |
| Quer só reproduzir o resultado | Cap. 4 + Cap. 8 (scripts) |
| Quer entender o argumento por trás | Cap. 1 + Cap. 5 + Cap. 6 |
| Está com pressa | Pule para [`capitulos/07-replicacao.md`](capitulos/07-replicacao.md) |

## Estrutura do repositório

```
Pesquisa-IA-Praxis/
├── README.md                       ← você está aqui
├── LICENSE                         ← CC BY-SA 4.0
├── capitulos/
│   ├── 00-prefacio.md
│   ├── 01-por-que-isso-importa.md
│   ├── 02-stack-de-ferramentas.md
│   ├── 03-setup.md
│   ├── 04-fluxo-integrado.md       ← ⭐ o coração do livro
│   ├── 05-analises-possiveis.md
│   ├── 06-armadilhas-aprendidas.md
│   ├── 07-replicacao.md
│   ├── 08-anexo-catalogo.md
│   └── 99-referencias.md
├── scripts/
│   ├── export_zotero_to_vault.py   ← 1.893 refs → notas .md
│   ├── analise_shift_v2.py         ← shift temático tech↔humanas↔pedagogia
│   ├── compare_cooccurrence.py     ← co-ocorrência RIS × Zotero
│   └── gen_candidatas.py           ← candidatas a thesaurus VOSviewer
├── exemplos/
│   ├── shift-tematico-exemplo.md
│   └── cooccurrence-exemplo.md
├── _meta/
│   └── imagens/                    ← mapas VOSviewer, screenshots Obsidian
└── _build/                         ← saídas geradas (docx, pdf)
```

## Como contribuir

Encontrou um erro? Tem uma armadilha nova pra adicionar? Adaptou para outra área (direito, engenharia, biologia)?

Abra um **issue** ou faça um **pull request** em https://github.com/ricamesq/pesquisa-ia-praxis.

## Licença

[![CC BY-SA 4.0](https://img.shields.io/badge/Licen%C3%A7a-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE)

Você pode copiar, redistribuir e adaptar este material, inclusive para fins comerciais, desde que:
- **Atribua** a autoria original (Ricardo Mesquita, Mestrado em Ciências e Matemática, Universidade Cruzeiro do Sul)
- **Compartilhe pela mesma licença** (CC BY-SA 4.0)

## Citação sugerida

```bibtex
@book{mesquita2026pesquisaia,
  title     = {Pesquisa IA Práxis: Um manual prático de letramento bibliométrico-computacional para pesquisadores em educação e saúde},
  author    = {Mesquita, Ricardo},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/ricamesq/pesquisa-ia-praxis},
  note      = {Versão 0.1, maio de 2026. Licenciado sob CC BY-SA 4.0.}
}
```

## Sobre o autor

Ricardo Mesquita é mestrando em Ciências e Matemática pela Universidade Cruzeiro do Sul (UNICSUL, 2026), com pesquisa em letramento digital docente e tecnologias de aprendizagem. Coordenador proposto do Núcleo de Inovação Tecnológica do CEUNSP (NIT-CEUNSP). Docente da Faculdade de Medicina do CEUNSP.

---

> 📚 **Próximo capítulo:** [00 — Prefácio](capitulos/00-prefacio.md)
