# Prestidígito ✦ O Tamanho Perfeito

Single-page app de medição de tamanho de anel para a Prestidígito (smartrings para mágicos).
Um único `index.html` — zero build, zero frameworks, fontes via Google Fonts.

## Como funciona a medição

**Ato I — calibração.** O usuário encosta uma carta de baralho poker (63,5 × 88,9 mm) na tela
e redimensiona uma carta virtual (slider, pinça ou botões ±1 px) até as bordas coincidirem.
A carta é ancorada no canto inferior esquerdo, então só há uma borda móvel por eixo.
A escala sai da **altura** (baseline mais longa → menor erro relativo):

```
ppm (px/mm) = altura_da_carta_em_px / 88,9
```

Alternativa para telas pequenas ou quem não tem baralho: cartão bancário ISO/IEC 7810 ID-1
(53,98 × 85,6 mm). A calibração persiste em `localStorage` (com o `devicePixelRatio` da época,
para avisar se a tela mudou).

**Ato II — medição.** Largura do dedo entre duas linhas-guia, ou diâmetro interno de um anel
existente sobre um círculo ajustável. Em ambos: `mm = px / ppm`.

**Ato III — conversões.**

```
circunferência = π × diâmetro
aro Brasil     = circunferência (mm) − 40        (arredondado ao inteiro)
tamanho US     = (diâmetro mm − 11,63) / 0,8128  (arredondado ao meio tamanho)
```

Sanidade: diâmetros fora de 13–24 mm disparam sugestão bem-humorada de recalibração.
