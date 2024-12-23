from collections import OrderedDict, defaultdict

import attr
from pathlib import Path
from pylexibank import Concept, Language, FormSpec
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import progressbar
import unicodedata

from lingpy import *
from clldutils.misc import slug

from tabulate import tabulate

from csvw.dsv import UnicodeWriter

@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)

class Dataset(BaseDataset):
    id = "lundgrenomagoa"
    dir = Path(__file__).parent
    concept_class = CustomConcept
    writer_options = dict(keep_languages=False, keep_parameters=False)
    
    def cmd_makecldf(self, args):

        args.writer.add_sources()
        
        # compute overlap with concept list that was officially submitted in
        # the thesis
        concepts = {}
        concept_mapper = {concept["CONCEPTICON_GLOSS"]: concept["ENGLISH"] for concept in
                self.concepts}
        mappings = {
                "AJÍ": ("ají, pepper", ),
                "ALSO~ALREADY" : ("already", ),
                "ANGRY" : ("angry, mad, be angry (intr)", ),
                "BACK" : ("back",),
                "BE FAT" : ("be fat",),
                "BE ODOROUS" : ("be odorous (fragrant) (intr)",),
                "BE SCARED" : ("be scared (v.), be afraid",),
                "BURST" : ("burst, break open",),
                "CANDELA~FIRE" : ("fire",),
                "CLOUD~FOG" : ("cloud",),
                "BEARD": ("beard, moustache, facial hair",),
                "CUTBANK" : ("cutbank, cliff, bluff",),
                "DRIP (INTR.)" : ("drip (intr.)", "drip (intr)"),
                "BENT": ("bent, humped", "bent, twisted", "bent, twisted@"),
                "DRY (V.)": ("dry (intr)", "dry (intr, trans)", "dry (trans)"),
                "ENCOUNTER": ("meet, encounter, come across, find",),
                "FAT~LARD": ("fat (lard)", ),
                "FELLOW MAN": ("fellow man", ),
                "FLAME (V.)": ("flame (v.), shine (as in giving off light)",
                               "flame (v.), shine, bright (as in giving off light)"),
                "FRIEND~LOVER": ("friend", "friend@", ),
                "COMPANION": ("friend, companion",),
                "FROG": ("frog, toad", "frog, toad, generic" ),
                "GO DOWNRIVER (INTR.)": ("go downriver (intr)", ),
                "GRAB": ("take, grab", ),
                "GRILL": ("grill", "grill, barbeque", "grill, barbeque (n)", 
                          "grill, barbqeue@"),
                "HIGH UP (ADV.)": ("high up (adv.)", ),
                "HURT": ("hurt", ),
                "LAND": ("land, ground, earth", ),
                "LARVA": ("larva, maggot, grub", ),
                "LEAVE (TR.)": ("leave (trans)", ),
                "LOSE WAY": ("lose way", ),
                "LOSE ONESELF": ("lose (oneself) (intr)", "lose (oneself), lose the way"),
                "NAIL (BODY PART)": ("fingernail", "toenail" ),
                "NAME": ("name (n.)", "name (n.)@" ),
                "NIGHT": ("night (evening)", ),
                "OWNER": ("owner, boss (master)", ),
                "PAINT~WRITE": (
                    "write, draw (intr, trans)",
                    "paint (intr, trans)", "write",  ),
                "PATH": ("path, road", ),
                "PATIO": ("patio (porch)", ),
                "PIT VIPER SP.": (
                    "snake sp., pit viper sp., Bothrops atrox", 
                    "snake sp., pit viper sp., Bothrops jararaca", 
                    "snake sp., pit viper sp., Lachesis muta" ),
                "PREY": ("prey", ),
                "RAIN": ("rain", "rain (n.)", "rain (v.) (intr)" ),
                "ROCK~SHAKE": ("rock, sway", "rock, sawy. for example, rock a baby" ),
                "SCRAPE (TR.)": ("scrape, scratch (trans)", ),
                "SMOKE FOOD": ("smoke food", ),
                "SORUBIM SP.": ("fish sp., sorubim sp., Pseudoplatystoma fasciatum", 
                                ),
                "SPILL~POUR": ("pour, spill", ),
                "STONE": ("stone, rock", ),
                "SOUND (V.)": ("emit noise, sound", ),
                "THROW": ("throw a spear, stab", "throw, throw away (trans)" ),
                "WORM~LARVA": ("earthworm", )
                }

        table = [["ID", "NUMBER", "ENGLISH", "LEXIBANK_GLOSS", "CONCEPTICON_ID",
                 "CONCEPTICON_GLOSS"]]
        args.log.info("prepare concept mapping")
        for concept in self.conceptlists[0].concepts.values():
            if concept.english in mappings:
                matches = mappings[concept.english]
            elif concept.concepticon_gloss in concept_mapper:
                matches = [concept_mapper[concept.concepticon_gloss]]
            else:
                matches = []
                args.log.warn("no concept found for {0}".format(concept.english))

            table += [[
                concept.id,
                concept.number,
                concept.english,
                " // ".join(matches),
                concept.concepticon_id,
                concept.concepticon_gloss,
                ]]
            cidx = "{0}_{1}".format(concept.number, slug(concept.english))
            for match in matches:
                concepts[match] = cidx
                args.writer.add_concept(
                        ID=cidx,
                        Number=concept.number,
                        Name=concept.english,
                        Concepticon_ID=concept.concepticon_id,
                        Concepticon_Gloss=concept.concepticon_gloss
                        )
        with UnicodeWriter(self.etc_dir / "concepts-refined.tsv",
                           delimiter="\t") as writer:
            for row in table:
                writer.writerow(row)
        args.log.info("Wrote corrected concept list to file.")

        args.writer.add_languages()
        
        wl = Wordlist(self.raw_dir.joinpath('lundgren_ma_analyzed_data.tsv').as_posix())
        for idx in progressbar(wl):
            if wl[idx, "concept"] in concepts:
                lexeme = args.writer.add_form_with_segments(
                        Local_ID=idx,
                        Language_ID=wl[idx, 'doculect'],
                        Parameter_ID=concepts[wl[idx, 'concept']],
                        Value=wl[idx, 'ipa'] or ''.join(wl[idx, 'tokens']),
                        Form=wl[idx, 'ipa'] or ''.join(wl[idx, 'tokens']),
                        Segments=[{'_': '+'}.get(x, x) for x in wl[idx, 'tokens']],
                        Source=['Lundgren2020']
                        )
                args.writer.add_cognate(
                        lexeme=lexeme,
                        Cognateset_ID=wl[idx, 'cogid'],
                        Alignment=wl[idx, 'alignment'],
                        Source=['Lundgren2020']
                        )
