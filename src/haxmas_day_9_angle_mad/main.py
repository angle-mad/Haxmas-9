from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Label
from textual.containers import Grid, Vertical, Center
from textual.screen import Screen
import datetime

class DayScreen(Screen):
    """Screen for a day of the advent calendar!"""
    
    CSS = """
    DayScreen {
        align: center middle;
    }
    
    #dialog {
        width: 50;
        height: auto;
        border: thick #800020;
        background: #d4af37;
        padding: 2;
        align: center middle;
    }
    
    #dialog Label {
        width: 100%;
        text-align: center;
        margin-bottom: 1;
        color: #222222;
    }
    
    #dialog Button {
        width: auto;
        background: #800020;
    }

    #dialog Button:hover {
        background: #a82315;
    }

    """

    gifts = {
        1: "React Workshop!",
        2: "A Fusering Workshop!",
        3: "Keyring with Onshape!",
        4: "Hono Backend!",
        5: "Full Stack App with Flask!",
        6: "3D Printable Ruler!",
        7: "Interactive Christmas Tree!",
        8: "Automating Cookie Clicker!",
        9: "TUI in Textual!",
        10: "No leeks :3",
        11: "No leeks :p",
        12: "Still no leeks :3c"
    }
    
    def __init__(self, day: int) -> None:
        self.day = day
        super().__init__()
    
    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label(f"Day {str(self.day)} Unlocked!")
            yield Label(f"Here's what's in day {str(self.day)}: {self.gifts.get(self.day)}")
            with Center():
                yield Button("Close", id="close")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()
        event.stop()

class AdventCalendarApp(App):
    """A Textual app for an advent calendar."""
    
    CSS = """
    Grid {
        grid-size: 4 3;
        grid-gutter: 1 2;
    }
    
    Grid Button {
        width: 100%;
        height: 100%;
        background: #a82315;
    }
    
    Grid Button:hover {
        background: #c62828;
    }
    
    Grid Button.opened {
        background: #26401e;
    }
    """

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("r", "reset_calendar", "Reset Calendar")]
    START_DATE = datetime.date(2025, 12, 13)
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Grid():
            for day in range(1, 13):
                yield Button(str(day), id=f"day-{day}")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        button = event.button
        day = str(button.label)
        unlock_day = self.START_DATE + datetime.timedelta(days=int(day) - 1)
        if datetime.date.today() < unlock_day:
            self.notify(f"You will be able to unlock day {day} on {unlock_day}")
            return None
        if not button.has_class("opened"):
            button.add_class("opened")
        self.push_screen(DayScreen(int(day)))
    
    def action_reset_calendar(self) -> None:
        """An action to reset the calendar."""
        for button in self.query(Button):
            button.remove_class("opened")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

def main():
    app = AdventCalendarApp()
    app.run()

if __name__ == "__main__":
    main()