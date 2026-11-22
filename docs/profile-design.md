# Rafael Analyst / Profile v2.4

## Direção visual

A composição aprovada do banner **não foi redesenhada**. A logomarca original RA + Rafael Analyst, preservada byte a byte em `assets/profile/brand/rafael-analyst-oficial.png`, permanece integrada ao hero animado. Não há duplicação do lockup no corpo.

O restante do README foi alinhado ao mesmo sistema de design: fundo quase preto, cinzas frios, acento verde restrito, contraste suficiente, tipografia editorial e pequenos elementos técnicos que comunicam a função de cada área. A comunicação evita rankings sem fonte, supostas métricas e títulos de senioridade autodeclarados.

## Componentes

| Componente | Implementação | Responsabilidade |
| --- | --- | --- |
| Hero | GIF e fallback PNG locais | Identidade e resumo técnico; conteúdo relevante também existe em texto |
| Navegação | SVGs clicáveis | Acesso aos capítulos, site, LinkedIn e contato |
| Capítulos | 5 SVGs estáticos | Hierarquia visual consistente |
| Campos de atuação | `focus.svg` | Diferenciar sistemas, automação e dados |
| Arquitetura | `architecture.svg` | Diagnóstico → contrato → implementação → operação |
| Projetos | 8 SVGs de cards | Distinguir os mecanismos de cada referência, não apenas repetir o mesmo desenho |
| Bastidores | 4 `<details>` HTML | Regras, falhas, segurança e decisões de arquitetura |
| Stack | Devicon CDN + texto | Ícones das linguagens e rótulos acessíveis |
| CI | Validador Python | Impedir links, assets ou hashes inesperados |

## Delimitação de segurança e veracidade

Os cards são links para repositórios públicos que contêm implementações de referência. Não equivalem ao código privado nem comprovam produção em cliente. O validador verifica integridade local e URLs declaradas, não a disponibilidade externa no momento do push.

Apenas `README.md`, `assets/profile`, scripts associados, documentação, requisitos e o workflow da validação são publicados pelo script. Arquivos privados, configurações, bases de clientes e dados de terceiros não fazem parte da distribuição.

## Reprodução

```powershell
py scripts/generate_visuals.py
py scripts/validate_profile.py --require-logo
```

O gerador padrão **não altera** `hero.gif`, `hero-still.png` ou a logomarca. Esses três arquivos têm SHA-256 fixado no validador para impedir alterações acidentais. Para regenerar o hero, existe um script opcional separado, `generate_hero.py`, que requer Pillow e fontes locais; o resultado pode variar entre sistemas. Esse trabalho exige revisão visual e atualização intencional dos hashes.

## Limites da plataforma

O GitHub usa GitHub Flavored Markdown e HTML sanitizado. Não é possível instalar CSS/JS de página no README. SVGs são imagens estáticas; animação do cabeçalho vem do GIF. Os cards de projetos ocupam uma única coluna para manter a tipografia legível em telas menores. Os temas do navegador podem alterar as bordas das tabelas nativas da seção de tecnologias.

Visualizações locais ou screenshots são prévias aproximadas, não garantia de paridade pixel a pixel com a renderização do GitHub.
