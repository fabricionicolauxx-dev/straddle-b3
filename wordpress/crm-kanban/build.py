"""Gera o conteúdo da página /crm/ (ID 974) para o WordPress.

O WordPress troca '&' por '&#038;' dentro do bloco HTML, o que quebra o JavaScript.
Por isso o script vai codificado em base64 e é executado por um carregador sem '&'.

Uso: CRM_API_URL=... CRM_TOKEN=... python3 build.py > /caminho/conteudo.html
(o token não fica no repositório, que é público)
"""
import base64, os, re, sys

html = open(os.path.join(os.path.dirname(__file__), 'page.html'), encoding='utf-8').read()
html = html.replace('__API_URL__', os.environ['CRM_API_URL']).replace('__TOKEN__', os.environ['CRM_TOKEN'])
m = re.search(r'<script>\n(.*)</script>', html, re.S)
b64 = base64.b64encode(m.group(1).encode('utf-8')).decode()
loader = '<script>new Function(new TextDecoder().decode(Uint8Array.from(atob("' + b64 + '"),c=>c.charCodeAt(0))))();</script>'
assert '&' not in loader
sys.stdout.write('<!-- wp:html -->\n' + html[:m.start()] + loader + html[m.end():] + '\n<!-- /wp:html -->')
