# Corpus App

This repository contains source code for [the Corpus app](https://dh.nb.no/run/korpus/) from DH-lab at the National Library of Norway (NLN).

The app allow users to tailor their own corpus of texts from NLN's collection and download metadata for the corpus as an Excel file. The Excel file can be uploaded in several of DH-lab's other apps for digital text analysis, e.g. to get concordances or calculate the relative frequency of collocations.

Corpus creation can be done for the following document types:
- digibok: Digitised books
- digavis: Digitised news
- digitidsskrift: Digitised journals
- digistorting: Digitised parliamentary documents
- digimanus: Digitised letters and manuscripts
- kudos: [Knowledge documents from the poublic sector](https://kudos.dfo.no/))
- nettavis: Web news ("online news")

## dhlab package and Streamlit

The app is built around the [`dhlab` package for python](https://pypi.org/project/dhlab/). `dhlab` provides various functionality to analyse text from NLN's digital collection, and a wrapper to get text data through our [Swagger API](https://api.nb.no/dhlab/).

The webapp is published using [Streamlit](https://www.streamlit.io).

