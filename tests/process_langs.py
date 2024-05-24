#%%

from pathlib import Path
from collections import Counter
import pandas as pd

#%%
langs= Path("../distinct_languages.csv").read_text().splitlines()

distinct_langs = [l for langstring in langs for lang in langstring.strip('"').split(" / ") for l in lang.split("/")]

langcounts = Counter(distinct_langs)

df = pd.read_html("marc_lang_codes.html", encoding="utf-8")[0]
# %%
df["deprecated"] = df.code.str.startswith("-")
# %%
df.code = df.code.str.replace("-", "")
# %%
#df.set_index('code')['language'].to_csv("marc_codes.csv", sep=";")

#%%
#marc_lookup = pd.read_csv("marc_codes.csv", sep=";").set_index('code')['language'].to_dict()
marc_lookup = df.set_index('code')['language'].to_dict()
#%%
langdict = {}
for language, count in langcounts.items():
    try:
        langdict[language] = marc_lookup[language]
    except KeyError:
        print(language, "not found")

with open("language_codes.csv", "w") as f:
    f.write("\n".join(";".join([k, str(v)]) for k,v in langdict.items()))
# %%
