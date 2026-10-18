""" --- ntrfaces.py --- """

# Holds custom interfaces.

import ventris.gstats as g
import ventris.ntrface as n
import gint

import classes
import layout

from iobjects import graphics
from iobjects import anims
from iobjects import daemons
from iobjects import objects
from iobjects import inputs
from iobjects import charmaps
from iobjects import filesys

# Default variables
dtheme = [(255,255,255)] + ([(0,0,0)] * 4)

# Layout class for the main screens
l = layout.Layout()

# Interface index for redirection
iindex = {}

# Intro interface
gen = classes.IGen()
gen.add("intro", anims.IntroA())
iindex["IntroI"] = gen.create()

# Welcome interface
gen = classes.IGen()
texts = ["Welcome to p3, a new shell paradigm for Python,","aimed to be simple, useful, and customizable.","We hope you enjoy how much you use it.","Hit [EXE] to begin your installation.",]

gen.add("title", graphics.TitleText(l.g(0, 1)))
gen.add("text", graphics.MultiLineText(l.g(0, 6), texts, layout=l))
gen.add("reroute", daemons.VarsSetD("UNameSetI"))
iindex["WelcomeToP3I"] = gen.create()

# Username setting interface
gen = classes.IGen()
wlst = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
texts = ["Set a username.", "It must be alphanumeric, 4-20 chars long.", "It must start with an alphabetic character."]
def fisalpha(string): return string[0].isalpha()

gen.add("title", graphics.TitleText(l.g(0, 1)))
gen.add("text", graphics.MultiLineText(l.g(0, 4), texts, layout=l))
gen.add("input", inputs.ThemedInputText(l.g(2, 9), l.g(0, 9), "", charmaps.DCHARMAP, varn="uin"))
gen.add("valid", objects.ValidatorText(l.g(0, 10), "uin", "PWordSetI", lengths=(4, 20), wlst=wlst, functs=[fisalpha]))
iindex["UNameSetI"] = gen.create()

# Password setting interface
gen = classes.IGen()
texts = ["Set a password.", "It must be 8-48 chars long.",]

gen.add("title", graphics.TitleText(l.g(0, 1)))
gen.add("text", graphics.MultiLineText(l.g(0, 4), texts, layout=l))
gen.add("input", inputs.ThemedInputText(l.g(2, 9), l.g(0, 9), "", charmaps.DCHARMAP, varn="pwin"))
gen.add("valid", objects.ValidatorText(l.g(0, 10), "pwin", "ThemeSetI", lengths=(8, 48),))
iindex["PWordSetI"] = gen.create()

# Theme setting interface
gen = classes.IGen()
texts = ["Choose a theme using the d-pad.", "(The theme can be changed at any time.)"]
txtdim = (l.x(1) - l.x(- 1), l.y(2) - l.y(0))

gen.add("title", graphics.TitleText(l.g(0, 1)))
gen.add("text", graphics.MultiLineText(l.g(0, 4), texts, layout=l))
gen.add("theme", objects.VarText(l.g(0, 7), "s", "theme", label=("Theme: ", "")))
gen.add("set", daemons.ThemeD())
gen.add("colors", graphics.ThemedColorSelect(l.g(1, 8), dtheme, spacing=l.padding[1], show=False, txtdim=txtdim))
gen.add("reroute", daemons.VarsSetD("FinishedSetI"))
iindex["ThemeSetI"] = gen.create()

# Setup finalization interface
gen = classes.IGen()
texts = ["You're all set!", "Hit [EXE] to go to the login screen."]

gen.add("title", graphics.TitleText(l.g(0, 1)))
gen.add("text", graphics.MultiLineText(l.g(0, 4), texts, layout=l))
gen.add("reroute", daemons.VarsSetD("LoginI"))
gen.add("setup", daemons.SetupD())
iindex["FinishedSetI"] = gen.create()

# Login screen
gen = classes.IGen()
gen.add("title", graphics.TitleText(l.g(0, 1)))
gen.add("tag", objects.VarText(l.g(0, 6), "s", "username", label=("Welcome, ", "!")))
gen.add("input", inputs.ThemedInputText(l.g(2, 8), l.g(0, 8), "", charmaps.OPTNCHARMAP, varn="@pwin", passchar="*", passtogg=True))
gen.add("valid", objects.ValidatorText(l.g(0, 10), "@pwin", "MainI", comp=("s", "password"), errors={"comp" : "incorrect password"}))
gen.add("text", graphics.ThemedText(l.g(0, 14), "Press [Menu] to shut down.", tind=4))
gen.add("shutdown", daemons.VarsSetD("ShutdownI", keylst=[gint.KEY_MENU]))
iindex["LoginI"] = gen.create()

# Shutdown interface
gen = classes.IGen()
texts = ["Thank you for using p3! We are saving your data.", "Please do not hit [AC]."]

gen.add("title", graphics.TitleText(l.g(0, 1)))
gen.add("text", graphics.MultiLineText(l.g(0, 4), texts, layout=l))
gen.add("shutdown", filesys.ShutdownD())
iindex["ShutdownI"] = gen.create()

# Main interface
gen = classes.IGen()
texts = ["Run", "Pinned", "Settings"]
values = ["RunI", "PinnedI", "SettingsI"]
keymap = {gint.KEY_EXE : "redirect", gint.KEY_ALPHA : "redirect"}
center = (l.xc(), l.y(4))
radius = l.y(4) - l.y(2)

gen.add("header", graphics.Header(l))
gen.add("clock", graphics.ThemedAnalogClock(center, radius))
gen.add("select", inputs.MultiSelectText(l.g(1, 7), texts, values, layout=l, keymap=keymap))
gen.add("exittext", graphics.ThemedText(l.g(1, 14), "[Menu] to shut down | [Exit] to log out", tind=4))
gen.add("logout", daemons.VarsSetD("LoginI", keylst=[gint.KEY_EXIT]))
gen.add("shutdown", daemons.VarsSetD("ShutdownI", keylst=[gint.KEY_MENU]))
iindex["MainI"] = gen.create()

# Run interface
gen = classes.IGen()

gen.add("header", graphics.Header(l))
gen.add("text", graphics.ThemedText(l.g(1, 2), "Run"))
gen.add("input", inputs.ThemedInputText(l.g(3, 4), l.g(1, 4), "", charmaps.DCHARMAP, varn="@run"))
gen.add("confirm", daemons.VarsSetD(True, key="@exe"))
gen.add("error", objects.VarText(l.g(1, 6), "v", "@err"))
gen.add("run", filesys.RunD())
gen.add("exittext", graphics.ThemedText(l.g(1, 14), "Press [Exit] to return to the menu.", tind=4))
gen.add("exit", daemons.VarsSetD("MainI", keylst=[gint.KEY_EXIT]))
iindex["RunI"] = gen.create()

# Pinned programs interface
gen = classes.IGen()
texts = ["[Exe] to run", "D-pad to toggle pins | [Exit] to return to menu"]
deadmap = {gint.KEY_LEFT: - 1, gint.KEY_RIGHT: 1}

gen.add("header", graphics.Header(l))
gen.add("text", graphics.ThemedText(l.g(1, 2), "Pinned"))
gen.add("pins", inputs.PinSelect(l.g(1, 4)))
gen.add("files", inputs.PinSelect(l.g(1, 5), files=True, keymap=deadmap))
gen.add("run", filesys.RunPinnedD())
gen.add("empty", objects.EmptyText(l.g(1, 4), "s", "pinned", label="You have no pinned programs.", tind=4))
gen.add("error", objects.VarText(l.g(1, 11), "v", "@err"))
gen.add("infotext", graphics.MultiLineText(l.g(1, 13), texts, layout=l))
gen.add("exit", daemons.VarsSetD("MainI", keylst=[gint.KEY_EXIT]))
iindex["PinnedI"] = gen.create()

# Settings interface
gen = classes.IGen()
texts = ["Change Username", "Change Password", "Set Theme"]
values = ["UNameI", "PWordI", "ThemeI"]
keymap = {gint.KEY_EXE : "redirect", gint.KEY_ALPHA : "redirect"}

gen.add("header", graphics.Header(l))
gen.add("text", graphics.ThemedText(l.g(1, 2), "Settings"))
gen.add("select", inputs.MultiSelectText(l.g(1, 4), texts, values, layout=l, keymap=keymap))
gen.add("setup", daemons.SetupD(override=True))
gen.add("exittext", graphics.ThemedText(l.g(1, 14), "[Exit] to return to main menu", tind=4))
gen.add("exit", daemons.VarsSetD("MainI", keylst=[gint.KEY_EXIT]))
iindex["SettingsI"] = gen.create()

# Username resetting interface
gen = classes.IGen()
texts = ["Choose a new username.", "It must be alphanumeric, 4-20 chars long.", "It must start with an alphabetic character."]

gen.add("header", graphics.Header(l))
gen.add("title", graphics.ThemedText(l.g(1, 2), "Set Username"))
gen.add("text", graphics.MultiLineText(l.g(1, 4), texts, layout=l))
gen.add("input", inputs.ThemedInputText(l.g(3, 9), l.g(1, 9), "", charmaps.DCHARMAP, varn="uin"))
gen.add("valid", objects.ValidatorText(l.g(1, 10), "uin", "SettingsI", lengths=(4, 20), wlst=wlst, functs=[fisalpha]))
gen.add("exittext", graphics.ThemedText(l.g(1, 14), "[Exit] to return to main menu", tind=4))
gen.add("exit", daemons.VarsSetD("SettingsI", keylst=[gint.KEY_EXIT]))
iindex["UNameI"] = gen.create()

# Password resetting interface
gen = classes.IGen()
texts = ["Set a new password.", "It must be 8-48 chars long.",]

gen.add("header", graphics.Header(l))
gen.add("title", graphics.ThemedText(l.g(1, 2), "Set Password"))
gen.add("text", graphics.MultiLineText(l.g(1, 4), texts, layout=l))
gen.add("input", inputs.ThemedInputText(l.g(3, 9), l.g(1, 9), "", charmaps.DCHARMAP, varn="pwin"))
gen.add("valid", objects.ValidatorText(l.g(1, 10), "pwin", "SettingsI", lengths=(8, 48),))
gen.add("exittext", graphics.ThemedText(l.g(1, 14), "[Exit] to return to main menu", tind=4))
gen.add("exit", daemons.VarsSetD("SettingsI", keylst=[gint.KEY_EXIT]))
iindex["PWordI"] = gen.create()

# Theme resetting interface
gen = classes.IGen()
texts = ["Choose a theme using the d-pad.", ]
txtdim = (l.x(1) - l.x(- 1), l.y(2) - l.y(0))

gen.add("header", graphics.Header(l))
gen.add("title", graphics.ThemedText(l.g(1, 2), "Set Theme"))
gen.add("text", graphics.MultiLineText(l.g(1, 4), texts, layout=l))
gen.add("theme", objects.VarText(l.g(1, 7), "s", "theme", label=("Theme: ", "")))
gen.add("set", daemons.ThemeD())
gen.add("colors", graphics.ThemedColorSelect(l.g(1, 8), dtheme, spacing=l.padding[1], show=False, txtdim=txtdim))
gen.add("reroute", daemons.VarsSetD("SettingsI"))
iindex["ThemeI"] = gen.create()