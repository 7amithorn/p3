""" --- inputs.py --- """

# Handles objects that take in user input.

import gint
import time
import ventris.ntrface as n

import graphics
import aux

dtheme = [(255,255,255)] + ([(0,0,0)] * 4)

class ThemedSAIndicator(n.ShiftAlphaIndicator):
  """A theme-modified version of ShiftAlphaIndicator."""
  
  def __init__(self, ul, size="small", txtdim=None, theme=dtheme):
    """Initialize values."""
    bcg, main, shc, alc, col = theme
    super().__init__(ul, shc, alc, col, bcg, size, txtdim)
    self.settheme(theme)
  
  def settheme(self, theme):
    """Set the theme."""
    self.shift.color, self.shift.select, self.shift.background = theme[4], theme[2], theme[0]
    self.alpha.color, self.alpha.select, self.alpha.background = theme[4], theme[3], theme[0]

class ThemedInputText(n.ShiftAlphaInputText):
  """
  A theme-modified version of ShiftAlphaInputText.
  Dumps input into vars[self.varn].
  Can also provide a cursor.
  """
  
  def __init__(self, ul, saul, label, charmap, maxlen=None, passchar="", theme=dtheme, size="small", history=False, varn="input", cursor=.5, passtogg=False):
    """Initialize values."""
    background, color, shiftcol, alphacol, descol = theme
    self.cursor = cursor
    super().__init__(ul, saul, label, charmap, maxlen, passchar, color, shiftcol, alphacol, descol, background, size, history)
    
    self.saind = ThemedSAIndicator(saul, size, theme=theme)
    self.varn = varn
    self.passtogg, self.opchar = passtogg, ""
    self.arg2command["<null>"] = self.unull
    if self.passtogg:
      self.arg2command["<optn>"] = self.uoptn
    self.settheme(theme)
  
  def settheme(self, theme):
    """Set the theme."""
    self.background, self.color = theme[0], theme[1]
    self.saind.settheme(theme)
  
  def update(self):
    """Update the visual input and history."""
    inlen = len(self.label + self.show) * self.txtdim[self.size][0]
    if inlen > self.maxlen:
      vinput = self.show[int((inlen - self.maxlen) / self.txtdim[self.size][0]) + 1 :]
    else:
      vinput = self.show
    if self.passchar:
      vinput = self.label + (self.passchar * len(vinput))
    else:
      vinput = self.label + vinput
    if self.cursor and int(time.time() / self.cursor) % 2 == 0:
      vinput += "|"
    self.change(vinput)
  
  def respond(self, event, settings, vars):
    """Respond to a single keypress."""
    ktype, key = event.type, event.key
    if ktype == gint.KEYEV_UP:
      try:
        val = super(ThemedInputText, self).respond(event)
      except n.KeymapError:
        pass
      else:
        vars[self.varn] = val
  
  def uoptn(self):
    """Toggle showing text, if allowed."""
    self.passchar, self.opchar = self.opchar, self.passchar
  
  def unull(self):
    """Placeholder function so lack of keys don't register."""
    pass

class MultiSelectText(graphics.MultiLineText):
  """
  Displays a column of lines of text that can be selected.
  Selection sets vars[self.varn] to the associated item in values.
  """
  
  def __init__(self, ul, textl, values, layout, keymap={gint.KEY_EXE : "redirect"}, theme=dtheme):
    """Initialize values."""
    super().__init__(ul, textl, layout, tclass=graphics.ThemedSelectText)
    self.keymap = keymap
    self.values = values
    self.iselect = 0
    self.movekeys = (gint.KEY_UP, gint.KEY_DOWN)
    self.toggle()
  
  def settheme(self, theme):
    """Set the theme of the text."""
    for text in self.texts:
      text.settheme(theme)
  
  def toggle(self):
    """Toggle the selected item."""
    self.texts[self.iselect].tglselect()
  
  def next(self, key):
    """Move to the next item."""
    self.toggle()
    inc = (self.movekeys.index(key) * 2) - 1
    self.iselect += inc
    self.uiselect()
    self.toggle()
  
  def uiselect(self):
    """"Update the index selection."""
    if self.iselect >= len(self.texts): self.iselect -= len(self.texts)
    if self.iselect < 0: self.iselect += len(self.texts)
  
  def respond(self, event, settings, vars):
    """Respond to a keypress."""
    ktype, key = event.type, event.key
    if ktype == gint.KEYEV_UP:
      if key in self.keymap:
        vars[self.keymap[key]] = self.values[self.iselect]
      elif key in self.movekeys:
        self.next(key)

class PaneledSelectText(MultiSelectText):
  """Displays panels of MultiSelectText objects."""
  
  def __init__(self, ul, imax, textl, values, layout, keymap={gint.KEY_EXE : "redirect"}, theme=dtheme):
    """Initialize values."""
    super().__init__(ul, textl, values, layout, keymap, theme)
    self.imax = imax
    self.movekeys = (gint.KEY_F5, gint.KEY_F6)
    self.__initlists()
  
  def __initlists(self, textl=None, values=None):
    """Define text lists."""
    if not textl: textl = self.textl
    if not values: values = self.values
    btextl = aux.lbreak(textl, self.imax)
    bvalues = aux.lbreak(values, self.imax)
    self.texts = [MultiSelectText(self.ul, pair[0], pair[1], self.layout, keymap=self.keymap, theme=dtheme) for pair in zip(btextl, bvalues)]
    self.settheme(self.theme)
  
  def panel(self):
    """Return the current panel."""
    return self.texts[self.iselect]
  
  def respond(self, event, settings, vars):
    """Respond to a keypress."""
    ktype, key = event.type, event.key
    if ktype == gint.KEYEV_UP:
      if key in self.movekeys:
        self.next(key)
      else:
        self.panel().respond(event, settings, vars)
  
  def toggle(self):
    """
    Since we're looking at only one panel at a time,
    toggling is useless.
    """
    pass
  
  def blit(self):
    """Draw the right panel."""
    self.panel().blit()
    
  def delete(self):
    """Delete the panel."""
    self.panel().delete()

class ModalSelect(graphics.ThemedText):
  """Displays a range of classes, allowing one to be selected, one at a time."""
  
  def __init__(self, ul, texts, vals, theme=dtheme, tind=1, keymap={gint.KEY_LEFT: - 1, gint.KEY_RIGHT: 1, gint.KEY_EXE: "exe"}, var="modal"):
    """Initialize values."""
    super().__init__(ul, "", theme, tind)
    self.texts, self.vals = texts, vals
    self.keymap = keymap
    self.var = var
    self.iselect = 0
    self.change(self.texts[self.iselect])
  
  def respond(self, event, settings, vars):
    """Respond to a keypress."""
    ktype, key = event.type, event.key
    if ktype == gint.KEYEV_UP and key in self.keymap:
      if type(self.keymap[key]) == int:
        self.iselect += self.keymap[key]
        if self.iselect >= len(self.texts): self.iselect -= len(self.texts)
        if self.iselect < 0: self.iselect += len(self.texts)
      elif self.keymap[key] == "exe":
        self.varset(vars)
    self.change(self.texts[self.iselect])
   
  def varset(self, vars):
    """
    Set the value of the correlated settings variable.
    If you don't want the modal to set a var, remove the kv pair with exe, or blank this function.
    """
    vars[var] = self.vals[self.iselect]

class PinSelect(ModalSelect):
  """Select a pinned program."""
  
  def __init__(self, ul, theme=dtheme, tind=1, keymap={gint.KEY_LEFT: - 1, gint.KEY_RIGHT: 1, gint.KEY_EXE: "exe"}, files=False):
    """Initialize values."""
    super().__init__(ul, [""], [""], theme=dtheme, tind=tind, keymap=keymap, var="ph")
    self.files = files
  
  def respond(self, event, settings, vars):
    """Respond to a keypress."""
    pins = list(settings["pinned"].keys())
    if not pins:
      pins = shows = [""]
    if self.files:
      shows = list(settings["pinned"].values())
    else:
      shows = pins
    self.texts, self.vals = shows, pins
    super().respond(event, settings, vars)
  
  def varset(self, vars):
    """Set the requisite variables."""
    vars["@run"] = self.vals[self.iselect]
    vars["@exe"] = True