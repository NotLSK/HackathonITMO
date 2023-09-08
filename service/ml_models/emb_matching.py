import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

class TitleMatcher(object):
    def __init__(self, base='/app/ml_models/base/itmo_meta_bars.csv', weight_path='/app/ml_models/weights/SentTrensformer_weights'):
        self.model = SentenceTransformer().load(weight_path)
        
        self.base = pd.read_csv(base)
        self.base['base_embs'] = self.embed_base()
        
    def match(self, sent):
        dist = []
        if not isinstance(sent, str):
            return None
        
        emb = self.model.encode(sent)
        
        for base_emb in self.base['base_embs'].values:
           dist.append(cos_sim(emb, base_emb))

        ind = np.argmax(dist)
        score = max(dist)
        if score < 0.85:
          return None, None, score.item()
        return ind, self.base.iloc[ind, 1], score.item()
        
    def embed_base(self):
        base_emb = []
        for e in self.base.analogue_name.tolist():
            emb = self.model.encode(e)
            base_emb.append(emb)
        return base_emb