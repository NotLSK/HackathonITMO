import cv2
import numpy as np

from .sale_checker import SaleChecker
from .price_tag_reader import PriceTagReader
from .bar_code_reader import read_barcode
from .shelf_reader import ShelfAnalyser
from .emb_matching import TitleMatcher
from .bar_code_matching import BarCodeMatching


class CVPipeline:
    def __init__(self) -> None:
        self.ShelfReader = ShelfAnalyser()
        self.salechecker = SaleChecker()
        self.pricetagreader = PriceTagReader()

    def process_price_tag(self, image):
        # img = self._get_image(path)
        image = np.array(image)
        pricetaginfo = self.get_price_tag_info(image) # name, price
        pricetaginfo['promo'] = self.is_on_sale(image)       
        pricetaginfo['barcode'] = read_barcode(image)

        return pricetaginfo

    def process_shelf(self, image):
        
        image = np.array(image)
        shelf = self.ShelfReader.count_objects(image)

        return shelf 
    
    def is_on_sale(self, img: np.ndarray):
        '''
        return: True if on sale else False
        '''
        return self.salechecker.is_sale(img)
    
    def get_price_tag_info(self, img: np.ndarray):
        '''
        return {'name': item_name,
                'price': price}
        '''
        return self.pricetagreader.recognize_price_tag(img)
    
class NLPPipeline:
    def __init__(self) -> None:
        self.emb_matcher = TitleMatcher()
        self.br_matcher = BarCodeMatching()

    def match_barcode(self, barcode):
        is_found, output_from_base = self.br_matcher.get_match(barcode=barcode)
        is_found = is_found < 2

        return is_found, output_from_base
    
    def match_name(self, name):
        ind, output_from_base, score = self.emb_matcher.match(name)
        is_found = True

        if ind is None:
            is_found = False

        return is_found, ind, output_from_base, score

    
    


