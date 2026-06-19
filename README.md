# Prestidígito — Atelier de Medidas

PWA de medição de tamanho de anel para a Prestidígito (smartrings para mágicos).
Estética de joalheria fina, medição com precisão real, instalável e offline.

**Produção:** https://saidsati.github.io/prestidigito-ring-sizer/

## Arquitetura

- `index.html` — app inteiro (HTML + CSS + JS embutidos). Sem build, sem frameworks.
- `manifest.webmanifest` — manifesto PWA (instalável, standalone, ícones).
- `sw.js` — service worker: app-shell cache-first + Google Fonts stale-while-revalidate → funciona offline.
- `icon*.png` / `icon.svg` — ícones do app (gerados por `make_icons.py`).
- `make_icons.py` — gera os PNGs (anel + estrela, supersampling 4×). Roda só na build, não no runtime.

## Como a precisão funciona (para auditar)

A **única fonte de erro relevante é a calibração px→mm**. Decisões para minimizá-la:

1. **Referência ISO.** O padrão é o **cartão de banco** (ISO/IEC 7810 ID-1: 85,60 × 53,98 mm),
   padronizado a 0,01 mm — mais confiável que uma carta de baralho (que varia entre fabricantes).
   A carta poker (63,5 × 88,9 mm) fica como alternativa.
2. **Mede pela borda longa.** `ppm = comprimentoEmPx / 85,60`. A borda longa dá a maior baseline,
   então o mesmo erro de ±1 px pesa menos no resultado.
3. **Âncora num canto.** O usuário alinha o canto físico ao ponto dourado uma vez; só a borda
   oposta se move. Menos graus de liberdade = menos erro.
4. **Controles finos.** Slider + arrasto de borda + pinça + botões ± (~0,2 mm por toque).

Calibração persiste em `localStorage` junto do `devicePixelRatio` e largura da janela; se a tela
mudar numa revisita, o app sugere recalibrar.

### Métodos de medição (ordenados por exatidão)

| Método | O que mede | Conversão | σ diâmetro |
|---|---|---|---|
| **Anel que serve** | Ø interno direto | `Ø = px/ppm` | 0,18 mm |
| **Tira de papel** | circunferência real do dedo | `Ø = (px/ppm) / π` | 0,28 mm |
| **Dedo na tela** | largura (1 eixo) — estimativa | `Ø ≈ px/ppm` | 0,50 mm |

A tira de papel captura a **circunferência verdadeira** (dedo é elíptico, não circular), por isso
é mais honesta que medir só a largura na tela.

### Conversões de tamanho

```
circunferência (mm) = π × Ø
Aro Brasil          = circunferência − 40
Tamanho US          = (circunferência − 36,537) / 2,5535   (arredondado ao ½)
```

O resultado mostra uma **margem honesta**: para anel/tira, a tolerância no diâmetro
(`± hypot(σ_método, σ_calibração)`); para o dedo, a faixa provável de aro. Como cada número de
aro equivale a só ~0,32 mm de diâmetro, a margem é o jeito honesto de não fingir exatidão.

**Sanidade:** Ø fora de 13–24 mm abre um aviso sugerindo recalibrar (quase sempre é a calibração).

## Robustez

- Viewport travado (`user-scalable=no`) + vigia de `visualViewport.scale` que avisa se a tela
  estiver com zoom (o zoom quebra a escala física).
- Tudo em px CSS; a calibração absorve a densidade real do dispositivo.

## Pedido (sem backend)

O resultado vira um link de WhatsApp e um e-mail com a medida preenchida, além de copiar/compartilhar.
Configure número e e-mail no objeto `CONFIG` no topo do `<script>` em `index.html`:

```js
const CONFIG = { whatsapp: '5511999999999', email: 'pedidos@prestidigito.com.br' };
```

Quando houver uma loja (Shopify/Nuvemshop/etc.), basta trocar o destino do botão por um link de
checkout com o tamanho na query — sem reescrever o resto.

## Rodar localmente

```bash
python -m http.server 8431 --directory .
# abra http://localhost:8431
```

> Service worker exige HTTPS (ou localhost). Em produção, o GitHub Pages já serve por HTTPS.
