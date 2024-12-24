from lingpy import *

def modify(form):
    new_form = form.strip()
    mods = {
            "kw": "kʷ",
            "gw": "gʷ",
            "ɡw": "gʷ",
            "ɡ": "g",
            }
    for k, v in mods.items():
        new_form = new_form.replace(k, v)
    return new_form

lookup = {
    ("Tupinamba", "after", "takɨpwéɾi"): "",
    ("Tupinamba", "all", "opaβĩ"): "",
    ("Tupinamba", "be odorous", "tɨapwana"): "",
    ("Kokama", "chest", "putja"): "",
    ("Tupinamba", "cook", "jɨβa"): "",
    ("Tupinamba", "defecate (intr.)", "kaʔapia"): "",
    ("Omagua", "drip (intr.)", "atukɨra"): "",
    ("Tupinamba", "dust∼sand", "kuj"): "",
    ("Tupinamba", "four", "iɾu"): "",
    ("Omagua", "garbage", "ɨtɨ"): "",
    ("Kokama", "give", "mi"): "",
    ("Omagua", "give", "mi"): "",
    ("Kokama", "hammock", "ini"): "",
    ("Omagua", "hammock", "ini"): "",
    ("Tupinamba", "heart", "ɲɨʔa"): "",
    ("Kokama", "hole", "kwaɾa"): "",
    ("Omagua", "hole", "kwaɾa"): "",
    ("Kokama", "liver∼heart", "pɨa"): "",
    ("Kokama", "lose oneself", "kajɨma"): "",
    ("Omagua", "lose oneself", "kajma"): "",
    ("Kokama", "name", "iɾa"): "",
    ("Omagua", "name", "iɾa"): "",
    ("Omagua", "rest (intr.)", "japɨtu"): "",
    ("Kokama", "shine (intr.)", "peɾa"): "",
    ("Omagua", "shine (intr.)", "pɪɾa"): "",
    ("Omagua", "split (tr.)", "pɪsɪ"): "",
    ("Tupinamba", "sound (v.)", "pũ"): "",
    ("Omagua", "sweat (intr.)", "sɨ ̃i"): "",
    ("Omagua", "tail", "sũi"): "",
    ("Tupinamba", "vulva", "tamatiʔá"): "amatiʔá",
    ("Tupinamba", "water", "tɨ"): "ɨ",
    ("Kokama", "wife", "miɾikʷa"): "miɾikwa",
    ("Tupinamba", "worm∼larva", "sɨsoka"): "ɨsoka",
    ("Kokama", "yesterday", "ikʷatʃi"): "ikwatʃi",
        }

data = csv2list("cognates.tsv")

wl = Wordlist("lundgren_ma_analyzed_data.tsv")

wl2_ = {0: ["doculect", "concept", "form", "cogid"]}
idx = 1
for row_ in data[1:]:
    row = dict(zip(data[0], row_))
    for taxon in wl.cols:
        if taxon not in row:
            print(taxon)
        if row.get(taxon, "").strip():
            wl2_[idx] = [taxon, row["CONCEPT"], row[taxon], row["NUMBER"]]
            idx += 1
wl2 = Wordlist(wl2_)

form2idx = {(wl[idx, "ipa"], wl[idx, "doculect"]): idx for idx in wl}
for idx, lang, tokens in wl.iter_rows("doculect", "tokens"):
    form = "".join(tokens)
    if (form, lang) not in form2idx:
        form2idx[form, lang] = idx
matches = []
for idx, lang, concept, form in wl2.iter_rows("doculect", "concept", "form"):
    looked = lookup.get((lang, concept, form), "")
    
    if looked and (looked, lang) in form2idx:
        form = looked

    if (form, lang) not in form2idx:
        if (modify(form), lang) in form2idx:
            matches += [1]
        else:
            print('    ("' + lang + '", "' + concept + '", "' + form + '"): "",')
            matches += [0]
    else:
        matches += [1]

print(sum(matches) / len(matches))
        
