from ui.styles.colors import TEXT_PRIMARY
from ui.styles.typography import FONT_SIZE_BODY

class CardBody:
    def __init__(self, title: str, preview: str):
        self.title = title
        self.preview = preview

    def render(self):
        return {
            "title": self.title,
            "preview": self.preview,
            "style": {
                "color": TEXT_PRIMARY,
                "fontSize": FONT_SIZE_BODY
            }
        }