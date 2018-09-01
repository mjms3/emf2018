""" Tildr Dating
"""
___name___         = "Tildr Dating"
___license___      = "MIT"
___dependencies___ = ["wifi", "http", "ugfx_helper", "sleep"]
___categories___   = ["Other"]
___bootstrapped___ = True

import app, buttons, ugfx, ugfx_helper
from tilda import Buttons

ugfx_helper.init()

ugfx.clear()
ugfx.text(5, 5, "Tildr", ugfx.BLACK)

while True:
   if buttons.is_triggered(Buttons.BTN_Menu):
        break

app.restart_to_default()
