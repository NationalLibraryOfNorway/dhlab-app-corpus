import streamlit as st
import pandas as pd
import datetime
import dhlab as dh
from io import BytesIO

### Parameters ###
max_size_corpus = 20000
max_rows = 1200
min_rows = 800
default_size = 10  # percent of max_size_corpus


def to_excel(df):
    """Make an excel object out of a dataframe as an IO-object"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    # worksheet = writer.sheets["Sheet1"]
    # writer.save()
    processed_data = output.getvalue()
    return processed_data


def v(x):
    "Turn empty string into None"
    if x != "":
        res = x
    else:
        res = None
    return res


def header():
    col_zero, col_two, col_three = st.columns([4, 1, 1])
    with col_zero:
        st.subheader("Definer et korpus med innholdsdata og metadata")
        link = "https://github.com/nationallibraryofnorway/dhlab-app-corpus"
        col_zero.markdown(
            f""" 
    <div style="display: flex; align-items: center; gap: 5px; margin-top: -20px;">
    <a href="{link}" target="_blank">
        <i class="fab fa-github fa-1x" style="color: #262730;"></i>
    </a>
    <a href="https://www.nb.no/dh-lab/kontakt/" target="_blank">
        <i style='font-size:15px; color: #262730;' class='fas'>&#xf0e0;</i>
    </a>
    
</div>
""",
            unsafe_allow_html=True,
        )

    with col_three:
        st.markdown(
            """<style>img {opacity: 0.6;}</style><a href="https://nb.no/dhlab"><img src="https://github.com/NationalLibraryOfNorway/DHLAB-apps/raw/main/corpus/DHlab_logo_web_en_black.png" style="width:250px"></a>""",
            unsafe_allow_html=True,
        )
    with st.expander("ℹ️ Appinfo"):
        # st.write("some text")
        st.markdown(
            """Med denne appen kan man lage et DHLAB-korpus av tekster fra Nasjonalbibliotekets samling. Et DHLAB-korpus gjør at man kan gjøre kvantitative analyser av tekstsamlinger som inkluderer opphavsrettsbeskyttet materiale. I stedet for å laste ned tekstene, får man en kode for hver tekst. Denne kan så lastes opp i andre DHLAB-apper for å gjøre analyser på den teksten. 

DHLAB tilbyr følgende ressurstyper:  
**Digibok**: Bøker fra Nasjonalbiblioteket  
**Digavis**: Aviser fra Nasjonalbiblioteket  
**Digitidsskrift**: Tidsskrift fra Nasjonalbiblioteket  
**Digistorting**: Stortingsdokumenter i NBs samling  
**Digimanus**: Brev og manuskripter  
**Kudos**: [Kunnskapsdokumenter i offentlig sektor](https://kudos.dfo.no/)  

Man kan gjøre et utvalg fra metadata som er tilgjengelig for hver ressurstype. Ved å laste det ned, kan man bruke det samme korpuset i andre apper fra DHLAB.
"""
        )


def input_fields():
    def row1(params):
        col1, col2, col3 = st.columns([1, 1, 3])

        with col1:
            params["doctype"] = st.selectbox(
                "Type dokument",
                [
                    "digibok",
                    "digavis",
                    "digitidsskrift",
                    "digimanus",
                    "digistorting",
                    "kudos",
                ],
                help="Dokumenttypene følger Nasjonalbibliotekets digitale typer",
            )

        with col2:
            lang = st.multiselect(
                "Språk",
                [
                    "nob",
                    "nno",
                    "dan",
                    "swe",
                    "sme",
                    "smj",
                    "fkv",
                    "eng",
                    "fra",
                    "spa",
                    "ger",
                ],
                # default = "nob",
                help="Velg fra listen",
                disabled=(params["doctype"] in ["digistorting"]),
            )
            params["langs"] = " AND ".join(list(lang))

            if params["langs"] == "":
                params["langs"] = None

        with col3:
            today = datetime.date.today()
            year = today.year
            params["years"] = st.slider("Årsspenn", 1810, year, (1950, year))

    def row2(params):
        # st.subheader("Forfatter og tittel") ###################################################
        cola, colb = st.columns(2)

        with cola:
            params["authors"] = st.text_input(
                "Forfatter",
                "",
                help="Feltet blir kun tatt hensyn til for digibok",
                disabled=(params["doctype"] in ["digavis", "digistorting"]),
            )

        with colb:
            params["title"] = st.text_input(
                "Tittel",
                "",
                help="Søk etter titler. For aviser vil tittel matche avisnavnet.",
                disabled=(params["doctype"] in ["digistorting"]),
            )

    def row3(params):
        # st.subheader("Meta- og innholdsdata") ##########################################################

        cold, cole, colf = st.columns(3)
        with cold:
            params["fulltext"] = st.text_input(
                "Ord eller fraser i teksten",
                "",
                help="Matching på innholdsord skiller ikke mellom stor og liten bokstav."
                " Trunkert søk er mulig, slik at demokrat* vil finne bøker som inneholder demokrati og demokratisk blant andre treff",
            )

        with cole:
            params["ddk"] = st.text_input(
                "Dewey desimaltall",
                "",
                help="Input matcher et deweynummer. For å matche hele serien føy til en `*`. Bruk OR for å kombinere: 364* OR 916*",
                disabled=(params["doctype"] in ["digistorting"]),
            )

        with colf:
            params["subject"] = st.text_input(
                "Emneord",
                "",
                help="For å matche på flere emner, skill med OR for alternativ"
                " og AND for begrense. Trunkert søk går også — for eksempel vil barne* matche barnebok og barnebøker",
                disabled=(params["doctype"] in ["digistorting"]),
            )

    params = {}

    row1(params)
    row2(params)
    row3(params)

    return params


def corpus_management(params):
    df_defined = False
    st.subheader(
        "Lag korpuset og last ned metadata"
    )  ######################################################################

    with st.form(key="my_form"):
        colx, col_order, coly = st.columns([2, 2, 4])
        with colx:
            limit = st.number_input(
                f"Maks antall, inntil {max_size_corpus}",
                min_value=1,
                max_value=max_size_corpus,
                value=int(default_size * max_size_corpus / 100),
            )
            #    limit = st.number_input(300)
        with col_order:
            ordertype = st.selectbox(
                "Metode for uthenting",
                ["first", "rank", "random"],
                help="Metode 'first' er raskest, og velger dokument etter hvert som de blir funnet, mens'rank' gir en rask ordning på dokumenter om korpuset er definert med et fulltekstsøk og sorterer på relevans, siste valg er 'random' som først samler inn hele korpuset og gjør et vilkårlig utvalg av tekster derfra.",
            )
        with coly:
            filnavn = st.text_input("Filnavn for nedlasting", "korpus.xlsx")

        submit_button = st.form_submit_button(
            label="Trykk her når korpusdefinisjonen er klar"
        )

        if submit_button:
            match params["doctype"]:
                case "digimanus":
                    df = dh.Corpus(
                        doctype=v(params["doctype"]),
                        author=v(params["authors"]),
                        fulltext=v(params["fulltext"]),
                        from_year=params["years"][0],
                        to_year=params["years"][1],
                        title=v(params["title"]),
                        limit=limit,
                        order_by=ordertype,
                    ).frame
                    columns = ["dhlabid", "urn", "authors", "title", "timestamp", "year"]

                case "digavis":
                    df = dh.Corpus(
                        doctype=v(params["doctype"]),
                        fulltext=v(params["fulltext"]),
                        from_year=params["years"][0],
                        to_year=params["years"][1],
                        title=v(params["title"]),
                        limit=limit,
                        order_by=ordertype,
                    ).frame
                    columns = ["urn", "title", "year", "timestamp", "city"]

                case "digitidsskrift":
                    df = dh.Corpus(
                        doctype=v(params["doctype"]),
                        author=v(params["authors"]),
                        fulltext=v(params["fulltext"]),
                        from_year=params["years"][0],
                        to_year=params["years"][1],
                        title=v(params["title"]),
                        subject=v(params["subject"]),
                        ddk=v(params["ddk"]),
                        lang=params["langs"],
                        limit=limit,
                        order_by=ordertype,
                    ).frame
                    columns = [
                        "dhlabid",
                        "urn",
                        "title",
                        "city",
                        "timestamp",
                        "year",
                        "publisher",
                        "ddc",
                        "langs",
                    ]

                case "digistorting":
                    df = dh.Corpus(
                        doctype=v(params["doctype"]),
                        fulltext=v(params["fulltext"]),
                        from_year=params["years"][0],
                        to_year=params["years"][1],
                        limit=limit,
                        order_by=ordertype,
                    ).frame
                    columns = ["dhlabid", "urn", "year"]

                case _:
                    df = dh.Corpus(
                        doctype=v(params["doctype"]),
                        author=v(params["authors"]),
                        fulltext=v(params["fulltext"]),
                        from_year=params["years"][0],
                        to_year=params["years"][1],
                        title=v(params["title"]),
                        subject=v(params["subject"]),
                        ddk=v(params["ddk"]),
                        lang=params["langs"],
                        limit=limit,
                        order_by=ordertype,
                    ).frame
                    columns = [
                        "dhlabid",
                        "urn",
                        "authors",
                        "title",
                        "city",
                        "timestamp",
                        "year",
                        "publisher",
                        "ddc",
                        "subjects",
                        "langs",
                    ]

            st.markdown(f"Fant totalt {len(df)} dokumenter")

            if len(df) >= max_rows:
                st.markdown(f"Viser {min_rows} rader.")
                st.dataframe(df[columns].sample(min(min_rows, max_rows)).astype(str))

            else:
                st.dataframe(df[columns].astype(str))

            df_defined = True

    if df_defined:
        if st.download_button(
            "Last ned data i excelformat",
            to_excel(df),
            filnavn,
            help="Åpnes i Excel eller tilsvarende",
        ):
            pass


def main():
    ## Page configuration
    st.set_page_config(
        page_title="Korpus",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">',
        unsafe_allow_html=True,
    )

    header()

    st.write("---")

    params = input_fields()

    corpus_management(params)


if __name__ == "__main__":
    main()
