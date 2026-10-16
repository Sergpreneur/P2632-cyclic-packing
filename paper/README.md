# Manuscript

`main.tex` is the author-controlled source of the English working preprint, currently version 0.2 (16 October 2026). `main.pdf` is built from that source.

To rebuild from the repository root:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Section 5 describes the Lean 4 source, its verification methods, and the native-vs-kernel evaluation trust distinction. Neither the manuscript nor the GitHub release claims `M* = 12` or `M* = 13`.
