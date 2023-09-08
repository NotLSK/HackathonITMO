import easyocr
from typing import Dict, Tuple, List


class PriceTagReader:
    def __init__(self):
        self.reader = easyocr.Reader(['ru', 'en'], gpu=True)

    def recognize_price_tag(self, image) -> Dict:

        recognition_result = self.reader.readtext(image)
        item_name = self.get_item_name(recognition_result)
        price = self.get_price(recognition_result)

        return {'name': item_name,
                'price': price}

    def get_item_name(self, recognition_result: Tuple[List, str, float]) -> str:
        
        filtered_words = []

        for line in recognition_result:
            word = line[1]
            n_digits = sum(c.isdigit() for c in word)
            if n_digits > len(word) / 2:
                break

            filtered_words.append(word)

        return ' '.join(filtered_words)

    def get_price(self, recognition_result: Tuple[List, str, float]) -> int:

        digit_lines_only = [line for line in recognition_result if self.is_digits_only(line[1])]
        if digit_lines_only:
            sorted_by_height_lines = sorted(digit_lines_only,
                                            key=lambda box: box[0][2][1] - box[0][1][1],
                                            reverse=True)
        
            return int(sorted_by_height_lines[0][1]) 

    def is_digits_only(self, line: str) -> bool:

        return sum(c.isdigit() for c in line) == len(line)