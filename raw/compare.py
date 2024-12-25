from lingpy import *
from collections import defaultdict

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
    ("Kokama", "chest", "putja"): "putia",
    ("Kokama", "give", "mi"): "jumi",
    ("Kokama", "hammock", "ini"): "tukʷini",
    ("Kokama", "hole", "kwaɾa"): "kakʷaɾamai",
    ("Kokama", "liver∼heart", "pɨa"): "pɨja",
    ("Kokama", "lose oneself", "kajɨma"): "ukajma",
    ("Kokama", "name", "iɾa"): "tʃiɾa",
    ("Kokama", "shine (intr.)", "peɾa"): "peɾata",
    ("Kokama", "chest", "putja"): "putjakwaɾa",
    ("Kokama", "hammock", "ini"): "tukini",
    ("Kokama", "hole", "kwaɾa"): "tʃikwaɾa tsu",
    ("Omagua", "drip (intr.)", "atukɨra"): "atukɨɾa",
    ("Omagua", "garbage", "ɨtɨ"): "ɨtɨpɨta",
    ("Omagua", "give", "mi"): "jumi",
    ("Omagua", "hammock", "ini"): "tukʷini",
    ("Omagua", "hole", "kwaɾa"): "kakʷaɾamai",
    ("Omagua", "lose oneself", "kajma"): "ukajɨma",
    ("Omagua", "name", "iɾa"): "ʃiɾa",
    ("Omagua", "rest (intr.)", "japɨtu"): "japɨtuka",
    ("Omagua", "shine (intr.)", "pɪɾa"): "pɪɾata",
    ("Omagua", "split (tr.)", "pɪsɪ"): "pɪsɪkaka",
    ("Omagua", "sweat (intr.)", "sɨ̃i"): "sɨNi",
    ("Omagua", "tail", "sũi"): "suNi",
    ("Tupinamba", "after", "takɨpwéɾi"): "akɨpʷéɾi",
    ("Tupinamba", "all", "opaβĩ"): "opaβĩNatu",
    ("Tupinamba", "be odorous", "tɨapwana"): "ɨapʷana",
    ("Tupinamba", "cook", "jɨβa"): "mojɨβa",
    ("Tupinamba", "defecate (intr.)", "kaʔapia"): "kaʔapiasó",
    ("Tupinamba", "dust∼sand", "kuj"): "ɨβɨkuj",
    ("Tupinamba", "four", "iɾu"): "iɾundɨk",
    ("Tupinamba", "heart", "ɲɨʔa"): "ɲɨʔã",
    ("Tupinamba", "sound (v.)", "pũ"): "pu",
    ("Tupinamba", "vulva", "tamatiʔá"): "amatiʔá",
    ("Tupinamba", "water", "tɨ"): "ɨ",
    ("Kokama", "wife", "miɾikʷa"): "miɾikwa",
    ("Tupinamba", "worm∼larva", "sɨsoka"): "ɨsoka",
    ("Kokama", "yesterday", "ikʷatʃi"): "ikwatʃi",
    ("Tupinamba", "swallow (v.)", "mokona"): "mokoNa",

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

form2idx = defaultdict(list)
for idx, ipa, lang in wl.iter_rows("ipa", "doculect"):
    form2idx[ipa, lang] += [idx]
for idx, lang, tokens in wl.iter_rows("doculect", "tokens"):
    form = "".join(tokens)
    if (form, lang) not in form2idx:
        form2idx[form, lang] += [idx]
        
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
        
