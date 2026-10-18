""" --- themes.py --- """

# Manages p3 themes.
# A theme is a tuple of these colors: (background, first primary, first secondary, second primary, second secondary)
# You can add your own themes by editing this file.

# Import modules.
from random import randint

class Themes():
  """Manage themes."""
    
  def __init__(self, tind=0, **themes):
    """Initialize values."""
    # A theme is a tuple of these colors: (bcgcol, txtcol, lnecol, shcol, scrcol)
    self.themes = themes
    self.tind = tind
  
  def nthemes(self):
    """Count how many themes there are."""
    return len(list(self.themes.keys()))
  
  def addtheme(self, name, theme):
    """Add a new theme."""
    self.themes[name] = theme
    
  def stind(self, name):
    """Change the theme to the one with name."""
    if name in self.themes.keys():
      self.tind = list(self.themes.keys()).index(name)
  
  def ctind(self, inc):
    """Change tind by a certain increment."""
    self.tind += inc
    if self.tind < 0:
      self.tind += self.nthemes()
    elif self.tind > self.nthemes() - 1:
      self.tind -= self.nthemes()
  
  def rtind(self):
    """
    Change the theme to a random one.
    Will not keep the theme the same.
    """
    self.ctind(randint(1, self.nthemes() - 1))
    
  def gettheme(self):
    """Get the tuple of colors that is the current theme."""
    return self.themes[self.getname()]
  
  def getname(self):
    """Get the theme name."""
    return list(self.themes.keys())[self.tind]

# Create the themes instance.
themes = Themes()

# BUILT IN THEMES
# light: plain Casio-inspired theme
themes.addtheme("light", ((255, 255, 255), (0, 0, 0), (127, 127, 127), (255, 0, 0), (0, 0, 0)))

# dark: dark version of light
themes.addtheme("dark", ((0, 0, 0), (255, 255, 255), (127, 127, 127), (0, 255, 255), (255, 255, 255)))

# sea: harmonious blue theme
themes.addtheme("sea", ((0, 0, 100), (100, 255, 255), (127, 127, 255), (0, 100, 255), (100, 255, 255)))

# verdant: lush green theme
themes.addtheme("verdant", ((200, 255, 150), (44, 176, 0), (22, 88, 0), (110, 75, 0), (55, 220, 0)))

# ventris: theme using ventris theme colors
themes.addtheme("ventris", ((210, 190, 230), (40, 0, 80), (127, 127, 127), (80, 0, 160), (124, 64, 184)))

# vistren: theme using dark ventris theme colors
themes.addtheme("vistren", ((40, 0, 80), (210, 190, 230), (127, 127, 127), (170, 150, 190), (146, 126, 166)))

# PClight: theme based on colors of Planet Casio v4.3 and v5 (light)
themes.addtheme("PClight", ((255, 255, 255), (0, 0, 0), (195, 0, 0), (125, 0, 0), (255, 0, 0)))

# PCdark: theme based on colors of Planet Casio v5 (dark)
themes.addtheme("PCdark", ((0, 0, 0), (255, 255, 255), (195, 0, 0), (127, 127, 127), (255, 0, 0)))

# prime: bright, primary color-based theme
themes.addtheme("prime", ((255, 255, 255), (255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)))

# CUSTOM THEMES
# To add a new theme, simply add follow the template:
# themes.addtheme(name, theme)
# If you put it after the @end directive, it may not be saved.
#@end