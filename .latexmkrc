
$pdf_mode = 1;
$out_dir  = 'build';
ensure_path('TEXINPUTS', './plantilla-uoc//', './design-system/latex//');

# bib2gls support for glossaries-extra
add_cus_dep('aux', 'glstex', 0, 'run_bib2gls');
sub run_bib2gls {
    my ($base) = @_;
    # Extract just the filename without directory path
    my $basename = (split '/', $base)[-1];
    return system("bib2gls --dir build --tex-encoding utf-8 \"$basename\"");
}