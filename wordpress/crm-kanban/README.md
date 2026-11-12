# CRM Kanban (página privada do site)

- `Code.gs`: Apps Script ligado à planilha "Leads Straddle B3" (projeto criado em 12/11/2026). Publicado como App da Web (executar como Fabricio, acesso: qualquer pessoa com o token).
  - GET `?token=` lista a aba CRM; POST `{acao:'atualizar'|'adicionar'}` grava.
  - `sincronizarFormulario` (a cada 10 min) copia leads novos da aba "Leads página inicial" para o CRM como "Novo".
  - O token real NÃO fica neste repositório (ele é público). Está só no script e na página protegida.
- `page.html`: conteúdo do bloco HTML da página privada (protegida por senha, noindex). Trocar `__API_URL__` e `__TOKEN__` antes de colar.
