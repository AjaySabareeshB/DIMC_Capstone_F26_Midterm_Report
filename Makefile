# Build the midterm report: `make` (needs tectonic: https://tectonic-typesetting.github.io)
main.pdf: main.tex refs.bib $(wildcard figures/*)
	tectonic main.tex

clean:
	rm -f main.pdf *.aux *.log *.bbl *.blg *.out
