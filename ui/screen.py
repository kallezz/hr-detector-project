class Screen:
    """Base class for all screens. Subclasses override what they need."""

    def enter(self):
        """Called when the screen becomes active."""

    def exit(self):
        """Called when leaving the screen (stop sampling, free resources)."""

    def handle_input(self, event):
        """Handle an Input event. Return a ScreenId to switch, or None."""
        return None

    def update(self):
        """Called every frame. Return a ScreenId to switch, or None."""
        return None

    def draw(self, display):
        """Draw the screen. Called every frame."""