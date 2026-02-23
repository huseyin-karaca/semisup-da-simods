# latexmkrc — Overleaf configuration for cross-document references
#
# Enables \externaldocument cross-references between article.tex and
# supplement.tex via the xr-hyper package.
#
# On Overleaf: set the main document to "article.tex" in project settings.

$pdf_mode = 1;

# Custom dependency: when article.tex needs supplement.aux (due to
# \externaldocument{supplement}), compile supplement.tex in draft mode
# to produce supplement.aux without generating a full PDF.
# The same rule applies symmetrically for supplement.tex needing article.aux.
add_cus_dep('tex', 'aux', 0, 'cus_dep_require_aux');

sub cus_dep_require_aux {
    my $file = $_[0];
    return system("pdflatex -interaction=batchmode -draftmode $file.tex");
}
