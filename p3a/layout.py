""" --- layout.py --- """

# Defines a class that generates clean grid layouts.

try:
  from ventris.gstats import PYE_TXT_DIM
  from ventris.allbase import setxline, setyline, SBR
except ImportError: # for testing only!
  PYE_TXT_DIM = (8, 11)
  SBR = (396, 224)
  def null(*i): return
  sethseg = setvseg = null

class Layout():
  """A class that manages a text-dimension-spaced grid layout."""
  
  def __init__(self, txtdim=PYE_TXT_DIM, padding=(3,3)):
    """Initialize values."""
    self.txtdim, self.padding = txtdim, padding
  
  def line(self, n, i):
    """
    Find the i coordinate of the nth line.
    Use None for the greatest i.
    """
    if n == None:
      return SBR[i] - self.padding[i]
    dist = (self.txtdim[i] * abs(n)) + (self.padding[i] * (abs(n) + 1))
    return (SBR[i] - dist) if n < 0 else dist
  
  def xline(self, n):
    """
    Find the x coordinate of the nth line.
    Use None for the right.
    """
    return self.line(n, 0)
  
  def yline(self, n):
    """
    Find the y coordinate of the nth line.
    Use None for the bottom.
    """
    return self.line(n, 1)
  
  def ongrid(self, r, c):
    """Give the point on the grid at (r, c)."""
    return self.xline(r), self.yline(c)
  
  def setgrid(self, dist=25):
    """Display the grid currently set."""
    for n in range(dist):
      sethseg(self.xline(n))
    for n in range(dist):
      setvseg(self.yline(n))
  
  def icenter(self, i):
    """Find the center on i."""
    return (self.line(0, i) + self.line(None, i)) / 2
  
  def xcenter(self):
    """Find the x coordinate for the center."""
    return self.icenter(0)
  
  def ycenter(self):
    """Find the y coordinate for the center."""
    return self.icenter(y)
  
  def center(self):
    """Find the center of the layout."""
    return self.xcenter(), self.ycenter()
  
  def space(self, i):
    """Find the space on i between two gridpoints."""
    return self.line(1, i) - self.line(0, i)
  
  def width(self):
    """Find the width of a grid rect."""
    return self.space(0)
  
  def height(self):
    """Find the height of a grid rect."""
    return self.space(1)
  
  # Aliases
  g = ongrid   # l.g
  x = xline    # l.x
  y = yline    # l.y
  l = line     # l.l
  xc = xcenter # l.xc
  yc = ycenter # l.yc
  c = center   # l.c
  ic = icenter # l.ic
  s = space    # l.s
  w = width    # l.w
  h = height   # l.h