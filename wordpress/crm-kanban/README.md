# CRM Kanban (página privada do site)

- `Code.gs`: Apps Script ligado à planilha "Leads Straddle B3" (projeto criado em 12/11/2026). Publicado como App da Web (executar como Fabricio, acesso: qualquer pessoa com o token).
  - GET `?token=` lista a aba CRM; POST `{acao:'atualizar'|'adicionar'}` grava.
  - `sincronizarFormulario` (a cada 10 min) copia leads novos da aba "Leads página inicial" para o CRM como "Novo".
  - O token real NÃO fica neste repositório (ele é público). Está só no script e na página protegida.
- `page.html`: conteúdo do bloco HTML da página privada (protegida por senha, noindex). Trocar `__API_URL__` e `__TOKEN__` antes de colar.

## Publicado (12/11/2026)

- Página: https://traderfabricionicolau.com.br/crm/ (ID 974), protegida por senha do WordPress, noindex e fora do sitemap pelo WPCode 966.
- App da Web: implantação `AKfycbwBqzyVOHec4tdbBHJpGOPi8yj0Y5IM7sCDhyrF6tIFsBzbYsmykVYSUXnuvww6nexeZQ`. Ao mudar o `Code.gs`, criar NOVA VERSÃO na mesma implantação (Implantar › Gerenciar implantações › editar), senão a URL muda.
- Conteúdo da página gerado por `build.py` (script em base64, porque o WordPress troca `&` por `&#038;`).
- Etapa "Quase fechando" adicionada ao menu suspenso da coluna Etapa (Tabela_1).
