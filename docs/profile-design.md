# RA Profile v2.2 — decisões e manutenção

## Objetivo

Ser uma vitrine técnica, não um currículo inflado ou um painel de estatísticas decorativas.

## Delimitação de funcionamento

- O GitHub renderiza Markdown e parte do HTML, incluindo `<details>`, links, tabelas e imagens; ele não executa JavaScript de terceiros no README.
- A animação do hero está em `assets/profile/hero.gif`. Sua versão estática de apoio é `hero-still.png`.
- Ilustrações e cards SVG são locais e não dependem de serviço externo; são gerados por `scripts/generate_visuals.py`.
- Ícones das linguagens são servidos pelo CDN do projeto Devicon. Se o CDN estiver indisponível, o nome da tecnologia continua aparecendo em texto no README. Marcas e logos das tecnologias pertencem aos titulares respectivos.
- As seções de bastidores usam `<details>` nativo do GitHub. Não há scripts, rastreamento nem dados pessoais de terceiros.
- Nenhum serviço externo é usado para gerar supostas métricas de commits, títulos de cargo ou status de produção.
- A logomarca original não é recriada: o script de publicação copia `ra-original.png` de um dos projetos já mantidos no computador do autor.

## Mudanças de conteúdo

1. Atualizar as descrições e URLs dos projetos diretamente no `README.md`.
2. Se o projeto card mudou de nome ou título, atualizar a lista `PROJECTS` em `scripts/generate_visuals.py` e regenerar os assets.
3. Executar `python scripts/validate_profile.py --require-logo` no repositório final, após incorporar a logo.
4. Revisar a renderização no GitHub, no tema claro, no tema escuro e no mobile.

## Recriar visuais

Requer Python 3.11+ e Pillow. O arquivo gerado não precisa da dependência para funcionar no GitHub.

```powershell
py -m pip install "Pillow>=10,<13"
py scripts/generate_visuals.py
```

O gerador procura fontes locais no Windows, Linux e macOS. Caso utilize uma instalação incomum, ajuste `pick_font` no script. Não distribua arquivos de fonte.

## Segurança de publicação

O script `publish.ps1` não executa `git add .`, não usa `push --force` e recusa prosseguir com alterações locais preexistentes. Faz backup do README anterior fora do repositório, valida o remoto esperado e exige confirmação explícita.

## Observações

- README do perfil é público, mesmo quando há conteúdo em outras áreas privadas da conta.
- Somente oito repositórios públicos foram verificados no momento desta versão. `conversa-studio` retornou 404 na verificação externa e deve ser acrescentado somente após confirmação de acesso público.
- O GIF é decorativo. Toda informação essencial também aparece em texto acessível no Markdown.
