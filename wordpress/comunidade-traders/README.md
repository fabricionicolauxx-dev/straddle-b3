# /comunidade-traders/ (página 950) — versão da /grupo-traders/ (365) para anúncios

- Sem cripto/BingX/BTC/USDT; botões vão direto ao convite do Discord (discord.com/invite/faFXky6hDc).
- Prova real: prints da BingX desfocados na própria imagem (canvas, 320px, blur 9px) + EUR/USD com blur CSS.
- Olho no canto da Prova real: tooltip estilo Discord, leva ao convite.
- noindex + fora do sitemap via WPCode 966:

```php
add_filter('wpseo_robots', function($r){ return is_page(950) ? 'noindex, follow' : $r; });
add_filter('wp_robots', function($r){ if (is_page(950)) { $r['noindex'] = true; $r['follow'] = true; unset($r['index']); } return $r; });
add_filter('wpseo_exclude_from_sitemap_by_post_ids', function($ids){ $ids[] = 950; return $ids; });
```

Pendente: trocar os 6 sitelinks da PMax (hoje → /grupo-traders/) para /comunidade-traders/ quando o experimento acabar.
