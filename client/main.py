""" Tildr Dating
"""
___name___         = "Tildr Dating"
___license___      = "MIT"
___dependencies___ = ["wifi", "http", "ugfx_helper", "sleep", "dialogs", "sim800", "database"]
___categories___   = ["Other"]
___bootstrapped___ = True

import app, buttons, ugfx, ugfx_helper, http, dialogs, sim800, database, ujson
from tilda import Buttons

running = True
api_url = "http://emf2018.us-east-2.elasticbeanstalk.com"

ugfx_helper.init()
ugfx.clear(ugfx.html_color(0x000000))

style = ugfx.Style()
style.set_enabled([ugfx.WHITE, ugfx.WHITE, ugfx.html_color(0x888888), ugfx.html_color(0x444444)])
style.set_background(ugfx.html_color(0x000000))
ugfx.set_default_style(style)

def render_splash_screen():
    ugfx.clear(ugfx.html_color(0x000000))
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
    while True:
        if buttons.is_triggered(Buttons.BTN_Menu):
            return False
        if buttons.is_triggered(Buttons.BTN_A):
            return True

def create_profile():
    name, age = "", ""
    while name == "":
        name = dialogs.prompt_text("What's your name?")
    while age == "":
        age = dialogs.prompt_text("What's your age?")
    tag_line = dialogs.prompt_text("Tell us your tagline:")
    looking_for = dialogs.prompt_text("And what you're looking for:")
    contact = dialogs.prompt_text("How should your matches contact you? :P")
    imei = sim800.imei()

    top_left_logo()
    ugfx.text(5, 100, "Creating profile...", ugfx.BLACK)

    profile = {
        'unique_identifier': imei,
        'username': name,
        'age': age,
        'tag_line': tag_line,
        'looking_for': looking_for,
        'contact': contact
    }

    profile_json = ujson.dumps(profile)

    try:
        http.post(api_url+'/create_user', json=profile).raise_for_status().close()
    except:
        ugfx.clear()
        ugfx.text(5, 100, "Error creating profile. Try again later. :(", ugfx.BLACK)
        return False

    database.set("tildr_profile", profile_json)

    return True


def get_profile():
    profile_json = database.get("tildr_profile")
    if profile_json is None:
        return None

    profile = ujson.loads(profile_json)
    return profile


def top_left_logo():
    ugfx.clear(ugfx.html_color(0x000000))
    try:
        logo = http.get("https://i.imgur.com/5HXmXBU.png").raise_for_status().content
        ugfx.display_image(0, 5, bytearray(logo))
    except:
        pass


def quit_loop():
    while True:
        if buttons.is_triggered(Buttons.BTN_Menu):
            return False


while running:

    profile = get_profile()

    if profile is None:
        render_splash_screen()
        if not run_splash_screen():
            break
        if not create_profile():
            continue

    top_left_logo()
    if not quit_loop():
        break

app.restart_to_default()
