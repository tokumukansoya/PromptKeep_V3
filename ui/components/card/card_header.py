from ui.styles.colors import BORDER_COLOR

class CardHeader:
    def __init__(self, title: str):
        self.title = title

    def render(self):
        return {
            "title": self.title,
            "style": {
                "borderColor": BORDER_COLOR
            }
        }