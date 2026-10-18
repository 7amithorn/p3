""" --- daemons.py --- """

# Handles objects that aren't drawn.

import gint

class VarsSetD():
  """
  Sets a value of vars on certain keypresses.
  The default is to redirect.
  """
  
  def __init__(self, value, key="redirect", keylst=[gint.KEY_EXE], clean=False):
    """Initialize values."""
    self.value, self.keylst, self.key = value, keylst, key
    self.clean = clean
  
  def respond(self, event, settings, vars):
    """Respond to keypresses."""
    if self.clean:
      vars[self.key] = ""
    ktype, key = event.type, event.key
    if ktype == gint.KEYEV_UP and key in self.keylst:
      vars[self.key] = self.value


class VarsTransD(VarsSetD):
  """Transfers a value from one variable to another upon certain keypresses."""
  
  def __init__(self, ikey, key="redirect", keylst=[gint.KEY_EXE], clean=False):
    """Initialize values."""
    super().__init__(None, key, keylst, clean=clean)
    self.ikey = ikey
  
  def respond(self, event, settings, vars):
    """Move variables."""
    ktype, key = event.type, event.key
    if ktype == gint.KEYEV_UP and key in self.keylst:
      vars[self.key] = vars.get(self.ikey, "")


class ThemeD():
  """Changes the theme in response to keypresses."""
  
  def __init__(self, default="light"):
    """Initialize values."""
    self.default = default
  
  def respond(self, event, settings, vars, themes):
    """Get keypresses and themes."""
    flag = False
    ktype, key = event.type, event.key
    if ktype == gint.KEYEV_UP:
      if key == gint.KEY_RIGHT:
        themes.ctind(1)
        flag = True
      elif key == gint.KEY_LEFT:
        themes.ctind(- 1)
        flag = True
      elif key == gint.KEY_DOWN:
        themes.stind(self.default)
        flag = True
      elif key == gint.KEY_UP:
        themes.rtind()
        flag = True
      if flag:
        vars["retheme"] = True
        settings["theme"] = themes.getname()


class SetupD():
  """
  Finish setup by setting the username and password.
  Also toggles the installation variable.
  """
  
  def __init__(self, override=False):
    """Initialize values."""
    self.override = override
    
  def respond(self, event, settings, vars):
    """Set settings."""
    if not settings["_isinstalled"] or self.override:
      settings["_isinstalled"] = True
      if vars.get("uin"):
        settings["username"] = vars["uin"]
        del vars["uin"]
      if vars.get("pwin"):
        settings["password"] = vars["pwin"]
        del vars["pwin"]