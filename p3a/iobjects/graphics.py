""" --- graphics.py --- """

# This module handles static graphics for p3.

# Import modules.
import ventris.allbase as f
import ventris.gstats as g
import ventris.ntrface as n
import ventris.timing as t

dtheme = [(255,255,255)] + ([(0,0,0)] * 4)

class TitleText():
  """
  This class handles the title text for p3.
  It draws "p3 PoC", with the "3" raised as an exponent.
  """
  
  def __init__(self, ul, rheight=6, theme=dtheme):
    """Initialize values."""
    textlst = ["p  PoC", "3"]
    rul = (ul[0] + n.TXT_DIM["medium"][0]), (ul[1] - rheight)
    self.texts = [g.DataText([ul, rul][num], textlst[num]) for num in range(len(textlst))]
    self.settheme(theme)
  
  def settheme(self, theme):
    """Set the object theme."""
    colors = [theme[1], theme[3]]
    for i in range(len(self.texts)):
      self.texts[i].color = colors[i]
      self.texts[i].background = theme[0]
  
  def blit(self):
    """Blit the title text."""
    for text in self.texts:
      text.blit()
  
  def delete(self):
    """Delete the title text."""
    for text in self.texts:
      text.delete()

class HorizontalBar():
  """
  This class handles a horizontal bar.
  It is used for headers and taskbars.
  """
  
  def __init__(self, y, theme=dtheme):
    """Initialize values."""
    self.y = y
    self.settheme(theme)
  
  def settheme(self, theme):
    """Set the bar's theme."""
    self.color = theme[2]
    self.background = theme[0]
  
  def blit(self):
    """Blit the bar."""
    f.sethseg(self.y, self.color)
  
  def delete(self):
    """Delete the bar."""
    f.sethseg(self.y, self.background)

class ThemedText(g.DataText):
  """Text that can be altered to match a theme."""
  
  def __init__(self, ul, text, theme=dtheme, tind=1):
    """Initialize values."""
    super().__init__(ul, text)
    self.tind = tind
    self.settheme(theme)
  
  def settheme(self, theme):
    """Set the class theme."""
    self.color, self.background = theme[self.tind], theme[0]


class ThemedSelectText(g.SelectText):
  """Color-changing text that can be altered to match a theme."""
  
  def __init__(self, ul, text, theme=dtheme, tinds=(1,3)):
    """Initialize values."""
    super().__init__(ul, text)
    self.tinds = tinds
    self.settheme(theme)
  
  def settheme(self, theme):
    """Set the class theme."""
    self.color, self.select, self.background = theme[self.tinds[0]], theme[self.tinds[1]], theme[0]
    
class MultiLineText():
  """
  Displays text over multiple lines.
  Takes a list of text.
  Uses the Layout class.
  """
  
  def __init__(self, ul, textl, layout, theme=dtheme, tind=1, tclass=ThemedText):
    """Initialize values."""
    self.ul, self.layout, self.textl, self.theme, self.tclass = ul, layout, textl, theme, tclass
    self.__inittexts()
    # No need to set themes here, as the line above did that.
  
  def __inittexts(self, textl=None):
    """Define texts."""
    if not textl: textl = self.textl
    self.texts = [self.tclass((self.ul[0], self.ul[1] + self.layout.y(i)), textl[i], theme=self.theme) for i in range(len(textl))]
  
  def settheme(self, theme):
    """Set theme for all text."""
    for text in self.texts:
      text.settheme(theme)
  
  def blit(self):
    """Blit all text."""
    for text in self.texts:
      text.blit()
  
  def delete(self):
    """Delete all text."""
    for text in self.texts:
      text.delete()

class ShadowedText(MultiLineText):
  """
  Displays text with a drop shadow.
  Technically overlays two of the same text.
  """
  
  def __init__(self, ul, text, theme=dtheme, tinds=(1,1), adj=(1,0)):
    """Initialize values."""
    nul = [ul[i] + adj[i] for i in (0, 1)]
    self.texts = [ThemedText((ul, nul)[i], text, theme=dtheme, tind=tinds[i]) for i in (0, 1)]

class ThemedColorSelect(n.ColorSelect):
  """A themed, more flexible single color selector."""
  
  def __init__(self, ul, theme, text="", textlen=None, show=True, spacing=1, size="small", txtdim=None):
    """Initialize values."""
    super().__init__(ul, theme, text, textlen, theme[3], theme[0], theme[4], show, spacing, size, txtdim)
    
  def settheme(self, theme):
    """Set the theme."""
    self.colors = theme
    self.color, self.background, self.outline = theme[3], theme[0], theme[4]

class ThemedDigitalClock(t.DigitalClock):
  """A themed digital clock."""
  
  def __init__(self, ul, theme=dtheme, size="small", zone="time", form="standard", caps=False):
    """Initialize values."""
    background, color = theme[0], theme[1]
    super().__init__(ul, color, background, size, zone, form, caps)
  
  def settheme(self, theme):
    """Set the class theme."""
    self.color, self.background = theme[1], theme[0]

class ThemedAnalogClock(t.PixelTickedClock):
  """A themeable analog clock."""
  
  def __init__(self, center, radius, theme=dtheme, ticknum=12, zone="time"):
    """Initialize values."""
    hscolor, bhcolor, lhcolor, shcolor, tickcolor = [(0, 0, 0)] * 5
    background = (255, 255, 255)
    super().__init__(center, radius, ticknum=12, hscolor=hscolor, bhcolor=bhcolor, lhcolor=bhcolor, shcolor=shcolor, tickcolor=tickcolor, background=background, zone=zone)
    self.settheme(theme)
  
  def delete(self, coordlst=None):
    """Delete traces of the hands, if allowed."""
    if coordlst:
      super().delete(coordlst)
  
  def settheme(self, theme):
    """Set the clock theme."""
    self.hscolor, self.colors = theme[4], (theme[3], theme[1], theme[1])
    self.tickcolor, self.background = theme[2], theme[0]

class Header():
  """Handles a header, with basic info."""
  
  def __init__(self, layout, theme=dtheme):
    """Initialize values."""
    self.bar = HorizontalBar(layout.y(1), theme)
    self.clock = ThemedDigitalClock(layout.g(0, 0), theme=theme)
    self.sysn = ThemedText(layout.g(-9, 0), "", theme=theme, tind=3)
    self.objs = self.clock, self.bar, self.sysn
  
  def respond(self, event, settings, vars):
    """Get the clock style and other settings."""
    if settings.get("cform", None):
      self.clock.form = settings["cform"]
    else:
      settings["cform"] = self.clock.form
    vert = settings["__version"]
    self.sysn.change(settings["__name"] + " " + ".".join([str(n) for n in vert[:3]]) + vert[3])
  
  def update(self):
    """Update the clock."""
    self.clock.update()
  
  def blit(self):
    """Blit all the objects."""
    for obj in self.objs:
      obj.blit()
  
  def settheme(self, theme):
    """Set the theme of all the objects."""
    for obj in self.objs:
      obj.settheme(theme)
  
  def delete(self):
    """Delete all the objects."""
    for obj in self.objs:
      obj.delete()