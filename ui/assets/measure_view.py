from config import Display


def draw_measure_view(display, title, bpm, footer, points):

    if bpm is None:
        bpm_text = "BPM: --"
    else:
        bpm_text = "BPM: {}".format(bpm)
    display.text(title, 0, 0)
    display.text(bpm_text, 0, Display.LINE_HEIGHT)
    _draw_graph(display, points)
    display.text(footer, 0, Display.HEIGHT - Display.LINE_HEIGHT)


def _draw_graph(display, points):
    
    if len(points) < 2:
        return
    low = min(points)
    span = max(max(points) - low, 1)
    bottom = Display.GRAPH_TOP + Display.GRAPH_HEIGHT - 1
    previous_y = 0
    for x, point in enumerate(points):
        y = bottom - (point - low) * (Display.GRAPH_HEIGHT - 1) // span
        if x > 0:
            display.line(x - 1, previous_y, x, y)
        previous_y = y