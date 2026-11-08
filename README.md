# Straddle B3

Estatística de reação das ações da B3: quando uma ação cai (ou sobe) X% num pregão, o que ela costuma fazer depois? A página mostra acerto, resultado, perda máxima e ganho médio de cada ação, e marca as que passam nas suas regras de operação.

Endereço do site, depois de publicado: **https://fabricionicolauxx-dev.github.io/straddle-b3/**

## Como funciona

- `site/index.html` é o site.
- `scripts/update.py` baixa os arquivos oficiais da B3 (séries históricas COTAHIST, anuais e diários) e gera `site/data/quotes.json`.
- `.github/workflows/atualizar.yml` roda esse script de segunda a sexta às 20h17 (Brasília), com uma segunda tentativa às 7h41 do dia seguinte, e publica o site no GitHub Pages. Nada fica dependendo do seu computador ligado.

## Publicar pela primeira vez

1. Crie um repositório **público** chamado `straddle-b3` na sua conta (o GitHub Pages grátis exige repositório público).
2. Envie os arquivos deste projeto para ele.
3. No repositório, abra **Settings › Pages** e, em **Build and deployment › Source**, escolha **GitHub Actions**.
4. Abra a aba **Actions**, clique em **Atualizar dados e publicar site** e depois em **Run workflow**. Em 2 a 4 minutos o site está no ar.

## Atualizar na hora

Na aba **Actions › Atualizar dados e publicar site › Run workflow**. No site, o botão **Atualizar dados** busca a versão mais recente já publicada.

## Avisos

- Os preços da B3 vêm sem ajuste de proventos. Em data-ex de dividendos a ação pode aparecer com uma queda que não foi real.
- O GitHub pausa rotinas agendadas de repositórios sem nenhuma alteração por 60 dias. Se isso acontecer, ele avisa por e-mail; basta clicar em **Enable workflow** na aba Actions.
- Estatística passada mostra frequência, não garante o próximo resultado.
