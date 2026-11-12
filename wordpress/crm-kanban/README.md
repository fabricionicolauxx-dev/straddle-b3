# CRM Kanban (página privada do site)

- `Code.gs`: Apps Script ligado à planilha "Leads Straddle B3" (projeto criado em 12/11/2026). Publicado como App da Web (executar como Fabricio, acesso: qualquer pessoa com o token).
  - GET `?token=` lista a aba CRM; POST `{acao:'atualizar'|'adicionar'}` grava.
  - `sincronizarFormulario` (a cada 10 min) copia leads novos da aba "Leads página inicial" para o CRM como "Novo".
  - O token real NÃO fica neste repositório (ele é público). Está só no script e na página protegida.
- Código do quadro: `site/crm/kanban.js` e `site/crm/kanban.css` (publicados no GitHub Pages a cada push, sem a chave).
- `wp-shell.html`: o bloco HTML da página /crm/. Trocar `__API_URL__`, `__TOKEN__` e `__V__` (versão, para furar o cache) antes de colar.

## Publicado (12/11/2026)

- Página: https://traderfabricionicolau.com.br/crm/ (ID 974), protegida por senha do WordPress, noindex e fora do sitemap pelo WPCode 966.
- App da Web: implantação `AKfycbwBqzyVOHec4tdbBHJpGOPi8yj0Y5IM7sCDhyrF6tIFsBzbYsmykVYSUXnuvww6nexeZQ`. Ao mudar o `Code.gs`, criar NOVA VERSÃO na mesma implantação (Implantar › Gerenciar implantações › editar), senão a URL muda.
- O JavaScript fica fora do WordPress porque ele troca `&` por `&#038;` dentro do bloco HTML e quebra o código.
- Lembretes: coluna J da aba CRM, formato `AAAA-MM-DD HH:MM|Tipo|Nota`. Alerta só dispara com a página aberta.
- Etapa "Quase fechando" adicionada ao menu suspenso da coluna Etapa (Tabela_1).
