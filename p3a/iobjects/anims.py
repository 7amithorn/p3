""" --- anims.py --- """

# Handles objects that handle the p3 animations.

# Import modules.
import ventris.calcs as c
import ventris.allbase as f
import ventris.gstats as g
import ventris.ntrface as n
import ventris.timing as t

import gint
import math
import time

import graphics

dtheme = [(255,255,255)] + ([(0,0,0)] * 4)

class LoadingA():
  """
  Handle the loading animation.
  This animation is three points pulsing in and out in a circle.
  Note: for (radius, ptradius), logo is (25, 6) and loading is (6, 2).
  """
  
  def __init__(self, center, radius, ptradius, speedf=25, theme=dtheme):
    """Initialize values."""
    self.center, self.radius, self.ptradius, self.speedf = center, radius, ptradius, speedf
    # NB that increasing speedf will slow the animation.
    self.angle = math.pi * (1 / 2)
    self.dist = self.radius
    self.rots = 0
    
    self.settheme(theme)
  
  def update(self):
    """Update the animation."""
    self.angle = (math.pi * (1 / self.speedf)) + self.angle
    if self.angle >= 2 * math.pi:
      self.angle -= 2 * math.pi
    self.rots += 1 / self.speedf
    self.dist = math.cos(self.angle - (math.pi / 3)) * self.radius
  
  def settheme(self, theme):
    """Change the theme of the animation."""
    self.colors = [theme[1]] * 3
    self.background = theme[0]
    
  def blit(self):
    """Blit the animation."""
    for num in range(3):
      coord = c.cround(tuple([((self.dist * [math.cos, math.sin][num2](self.angle + ((2 / 3) * math.pi * num))) + self.center[num2]) for num2 in range(2)]))
      f.setfcir(coord, 0, self.ptradius, self.colors[num])
  
  def delete(self):
    """Delete the animation."""
    for num in range(3):
      coord = c.cround(tuple([((self.dist * [math.cos, math.sin][num2](self.angle + ((2 / 3) * math.pi * num))) + self.center[num2]) for num2 in range(2)]))
      f.setfcir(coord, 0, self.ptradius, self.background)


class IntroA():
  """
  Handles the opening animation.
  Combines LoadingA and TitleText.
  Also serves as a daemon.
  """
  
  def __init__(self, radius=25, ptradius=4, center=(((f.SBR[0] + f.SUL[0]) / 2), ((f.SBR[1] + f.SUL[1]) / 2)), movement=(5 * n.TXT_DIM["medium"][0]), mfact=12, showtime=2, theme=dtheme):
    """Initialize values."""
    self.radius, self.center, self.movement, self.mfact = radius, center, (radius + movement / 2), mfact
    self.loading = LoadingA(center, radius, ptradius, speedf=25)
    self.title = graphics.TitleText(((center[0] + radius + 5 - movement), center[1]))
    self.moveind, self.titleflag = self.movement, False
    self.showtime, self.showtimer, self.starttimer = showtime, 0, 0
    self.settheme(theme)
  
  def settheme(self, theme):
    """Set the animation theme."""
    self.loading.settheme(theme)
    self.title.settheme(theme)
  
  def update(self):
    """Update the animation."""
    if self.loading.rots < 3:
      self.loading.update()
    elif self.moveind > 0:
      mdist = self.movement / self.mfact
      self.loading.center = (self.loading.center[0] - mdist, self.loading.center[1])
      self.moveind -= mdist
    else:
      self.titleflag = True
  
  def respond(self, event, settings, vars):
    """Set up the two-second wait and redirect for the intro."""
    if event.type == gint.KEYEV_UP and event.key == gint.KEY_F6:
      self.redirect(settings, vars)
    if self.titleflag:
      if not self.starttimer:
        self.starttimer = time.time()
      self.showtimer = time.time()
      if self.showtimer - self.starttimer > self.showtime:
        self.redirect(settings, vars)
  
  def redirect(self, settings, vars):
    """Determine the redirect based on the login."""
    if settings["_isinstalled"]:
      vars["redirect"] = "LoginI"
    else:
      vars["redirect"] = "WelcomeToP3I"
  
  def blit(self):
    """Blit the loading animation."""
    if self.titleflag:
      self.title.blit()
    self.loading.blit()
  
  def delete(self):
    """Delete the animation"""
    if self.titleflag:
      self.title.delete()
    self.loading.delete()