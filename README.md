# A Unified Analysis of Generalization and Sample Complexity for Semi-Supervised Domain Adaptation

**Elif Vural, Hüseyin Karaca** — In preparation for submission to SIAM Journal on Mathematics of Data Science (SIMODS)


## File Overview

| File / Folder | Description |
|---|---|
| `article.tex` | Main manuscript |
| `supplement.tex` | Supplementary material (proofs) |
| `shared.tex` | Shared preamble (title, authors, common packages/macros, math symbols) included by both documents |
| `response.tex` | Reviewer comments from previous submission and list of corresponding revisions |
| `refs.bib` | Bibliography |
| `siamonline250211.cls` | SIAM document class |
| `siamplain.bst` | SIAM bibliography style |
| `docsiamonline.pdf` | SIAM author documentation |
| `figures/` | All figures |
| `latex_output/` | Local build output (PDFs, aux files, logs) |
| `previous_versions/` | Archived earlier drafts |
| `.vscode/` | VS Code / LaTeX Workshop settings for local use |


## Local Use (VS Code + LaTeX Workshop)

A .vscode/ folder is included with settings pre-configured for the [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) extension. 
Build outputs are directed to `latex_output/`.

A LaTeX distribution (e.g., MacTeX, TeX Live, or MiKTeX) must be installed on your system.
The configuration assumes that `latexmk`, `pdflatex`, and `bibtex` are available in `/Library/TeX/texbin/` (default MacTeX path on macOS).

No extra VS Code setup is required — open the folder in VS Code and compile `article.tex` or `supplement.tex` directly.


## Overleaf

The [Overleaf project](https://www.overleaf.com/5828151487npbrscqrknjt#a4c8bb) is linked to the GitHub repository **[huseyin-karaca/semisup-da-simods](https://github.com/huseyin-karaca/semisup-da-simods)** and syncs from it.

**Set the main document** to `article.tex` in Overleaf's Menu → Main document.

### Cross-referencing and `.aux` files

`article.tex` and `supplement.tex` reference each other's labels (section names, theorem numbers, etc.) via `\externaldocument` from the `xr-hyper` package. This requires each document's `.aux` file to be present when the other is compiled.

Unlike local builds, Overleaf does not persist `.aux` files between projects. As a workaround, copies of `article.aux` and `supplement.aux` are kept manually in the repository and uploaded to Overleaf. **If labels or section structure change, these files must be updated.**

For a step-by-step guide on how to do this, see:
[How to reference supplementary material in Overleaf](https://lukegloege.medium.com/how-to-reference-supplementary-material-in-overleaf-ddc415511ad7)


