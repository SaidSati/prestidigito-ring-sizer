# OBVIOUS — Medidor de Anel

PWA de medição de tamanho de anel da **OBVIOUS Enterprises** (smartrings).
Estética brutalista "forjado em lava", medição com precisão real, instalável e offline.

**Produção:** https://saidsati.github.io/prestidigito-ring-sizer/

## Arquitetura

- `index.html` — app inteiro (HTML + CSS + JS embutidos). Sem build, sem frameworks.
- `manifest.webmanifest` — manifesto PWA (instalável, standalone, ícones, tema obsidiana).
- `sw.js` — service worker: app-shell cache-first + Google Fonts stale-while-revalidate → offline.
- `icon*.png` / `icon.svg` — logo OBVIOUS (hexágono com furo) em brasa; gerados por `make_icons.py`.
- `make_icons.py` — gera os PNGs (Pillow). Roda só na build, não no runtime.

## Design

Brutalista / forja vulcânica: obsidiana (#0a0a0c), brasa (#ff5a1f), tipografia **Archivo** (900,
caixa alta) + **Space Grotesk**. O hero tem uma **forja procedural em canvas** (`#lava`): um anel
incandescente em segmentos com pulso de calor + brasas subindo, ~60fps, leve, offline, e que
respeita `prefers-reduced-motion` (desenha um quadro estático). A animação só roda na tela inicial
para poupar bateria. O logo é o hexágono OBVIOUS (porca/anel) recriado em SVG vetorial.

> Placeholder até as fotos chegarem: o "anel-herói" é um anel incandescente procedural. Quando as
> fotos do anel real forem enviadas, ele é trocado pelo produto com tratamento de brasa, e entra o
> **AR try-on** (câmera) — ver seção Câmera.

## Instalação (PWA) — iOS e Android

- **Android/Chrome:** usa `beforeinstallprompt` → botão "Instalar" + barra flutuante.
- **iOS/Safari:** o iOS **não** dispara prompt automático. O app detecta iPhone e abre uma folha com
  instruções: Compartilhar → "Adicionar à Tela de Início". Detecta também navegador não-Safari (Chrome
  iOS / apps) e avisa para abrir no Safari. Requer HTTPS (o GitHub Pages já fornece).
- Se já estiver instalado (`display-mode: standalone`), some com toda a UI de instalação.

## Câmera (status)

A medição **não usa câmera de propósito** — medir por contato na tela é mais preciso (sem erro de
perspectiva). A câmera entrará como **espetáculo de pitch**, não como medida:
- **AR try-on** (anel na mão) — planejado, depende das fotos do anel + lib de rastreamento de mão.
- Medição por foto fica como extra opcional rotulado "estimativa".

## Precisão (para auditar)

A única fonte de erro relevante é a calibração px→mm.

1. **Referência ISO** — cartão de banco (ISO/IEC 7810 ID-1: 85,60 × 53,98 mm), padronizado a 0,01 mm.
   Carta de baralho (63,5 × 88,9 mm) como alternativa.
2. **Borda longa** — `ppm = comprimentoPx / 85,60` (maior baseline = menor erro relativo).
3. **Âncora num canto** — só uma borda se move; menos graus de liberdade.
4. Slider + arrasto de borda + pinça + botões ± (~0,2 mm/toque). Persiste em `localStorage` com
   `devicePixelRatio`/largura; avisa para recalibrar se a tela mudar.

### Métodos (por exatidão)

| Método | Mede | Conversão | σ diâmetro |
|---|---|---|---|
| Anel que serve | Ø interno | `Ø = px/ppm` | 0,18 mm |
| Tira de papel | circunferência real | `Ø = (px/ppm)/π` | 0,28 mm |
| Dedo na tela | largura (estimativa) | `Ø ≈ px/ppm` | 0,50 mm |

### Conversões

```
circunferência = π × Ø
Aro Brasil     = circunferência − 40
Tamanho US     = (circunferência − 36,537) / 2,5535   (½ em ½)
```

Resultado mostra margem honesta (tolerância de diâmetro p/ anel/tira; faixa de aro p/ dedo).
Sanidade: Ø fora de 13–24 mm sugere recalibrar.

## Configuração de pedido

Sem backend: o resultado gera link de WhatsApp + e-mail + copiar. Edite no topo do `<script>`:

```js
const CONFIG = { whatsapp: '5511999999999', email: 'contato@obvious.enterprises' };
```

## Rodar localmente

```bash
python -m http.server 8431 --directory .
```
