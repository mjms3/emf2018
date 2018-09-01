""" Tildr Dating
"""
___name___         = "Tildr Dating"
___license___      = "MIT"
___dependencies___ = ["wifi", "http", "ugfx_helper", "sleep"]
___categories___   = ["Other"]
___bootstrapped___ = True

import app, buttons, ugfx, ugfx_helper, http
from tilda import Buttons

running = True

ugfx_helper.init()
ugfx.clear(ugfx.html_color(0x000000))

style = ugfx.Style()
style.set_background(ugfx.html_color(0x000000))
ugfx.set_default_style(style)


def render_splash_screen():
    try:
        logo = http.get("https://i.imgur.com/0TjxEPs.png").raise_for_status().content
        ugfx.display_image(
            int((ugfx.width() - 164)/2),
            20,
            bytearray(logo))
    except:
        pass

    ugfx.text(160, 100, "TILDR", ugfx.WHITE)
    ugfx.text(0, 270, "Find your match @emfcamp ;)", ugfx.WHITE)
    ugfx.text(45, 300, "Press A to begin", ugfx.WHITE)


def run_splash_screen():
    global running
    while True:
        if buttons.is_triggered(Buttons.BTN_Menu):
            running = False
            break
        if buttons.is_triggered(Buttons.BTN_A):
            break


while running:
    render_splash_screen()
    run_splash_screen()

app.restart_to_default()
