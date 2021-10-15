from rfidsecuritysvc.model import BaseModel


class Color(BaseModel):
    def __init__(self, color):
        self.int = color
        # The color is stored as an integer, convert it to a hex string (e.g. FFFFFF)
        # and an HTML hex string (e.g. #ffffff) for use in various contexts
        self.hex = '{:06X}'.format(color)
        self.html = f'#{"{:06x}".format(color)}'
