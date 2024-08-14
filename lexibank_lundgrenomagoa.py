from collections import OrderedDict, defaultdict

import attr
from pathlib import Path
from pylexibank import Concept, Language, FormSpec
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import progressbar
import unicodedata

from lingpy import *
from clldutils.misc import slug

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

        # add concepts from list
        concepts = {}
        for concept in self.concepts:
            cid = '{0}_{1}'.format(concept['NUMBER'], 
                    slug(concept['ENGLISH']))
            args.writer.add_concept(
                    ID=cid,
                    Number=concept['NUMBER'],
                    Name=concept['ENGLISH'],
                    Concepticon_ID=concept["CONCEPTICON_ID"],
                    Concepticon_Gloss=concept["CONCEPTICON_GLOSS"])
            concepts[concept["ENGLISH"]] = cid

        args.writer.add_languages()
        
        wl = Wordlist(self.raw_dir.joinpath('lundgren_ma_analyzed_data.tsv').as_posix())
        for idx in progressbar(wl):
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
