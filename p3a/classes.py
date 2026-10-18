""" --- classes.py --- """

# Defines base classes for p3.

class Interface():
  """
  Defines an interface.
  Interfaces serve as containers for objects.
  """
  
  def __init__(self, components, settings, vars, themes):
    """Initialize values."""
    self.components, self.settings, self.vars, self.themes = components, settings, vars, themes
  
  def blit(self):
    """Blit every component."""
    for comp in self.components.values():
      try:
        comp.blit()
      except AttributeError as err:
        if "'blit'" not in str(err).split():
          # Catch attribute errors that aren't this function's.
          raise err
  
  def delete(self):
    """Delete every component."""
    for comp in self.components.values():
      try:
        comp.delete()
      except AttributeError as err:
        if "'delete'" not in str(err).split():
          # Catch attribute errors that aren't this function's.
          raise err
  
  def settheme(self):
    """Change the theme of every component."""
    self.themes.stind(self.settings["theme"])
    for comp in self.components.values():
      try:
        comp.settheme(theme=self.themes.gettheme())
      except AttributeError as err:
        if "'settheme'" not in str(err).split():
          # Catch attribute errors that aren't this function's.
          raise err
      
  def fullblit(self):
    """Fullblit every component."""
    for comp in self.components.values():
      try:
        comp.fullblit()
      except AttributeError as err:
        if "'fullblit'" not in str(err).split():
          # Catch attribute errors that aren't this function's.
          raise err
  
  def update(self):
    """Update every component."""
    for comp in self.components.values():
      try:
        comp.update()
      except AttributeError as err:
        if "'update'" not in str(err).split():
          # Catch attribute errors that aren't this function's.
          raise err
  
  def respond(self, event):
    """
    Get a response for an event from every component.
    Can also give the themes to daemons.
    """
    exitval = None 
    for comp in self.components.values():
      try:
        exitval = comp.respond(event, self.settings, self.vars)
        if exitval == - 1:
          return exitval
      except TypeError:
        try:
          # Theme changers do not have permission to close the system.
          comp.respond(event, self.settings, self.vars, self.themes)
        except TypeError:
          # Something is wrong with the function.
          comp.respond(event, self.settings, self.vars)
      except AttributeError as err:
        if "'respond'" not in str(err).split():
          # Catch attribute errors that aren't this function's.
          raise err

class IGen():
  """Generates interface objects so they can be customized."""
  
  def __init__(self, **components):
    """Initialize values."""
    self.components = components
  
  def add(self, name, obj):
    """Add a new component."""
    self.components[name] = obj
  
  def delete(self, name):
    """Delete a component."""
    del self.components[name]
  
  def create(self):
    """Make a generator function to be used to create instances."""
    comps = self.components
    
    def _create_intf(settings, vars, themes):
      """Generate a customized interface."""
      nonlocal comps
      return Interface(comps, settings, vars, themes)
    
    return _create_intf

# Set basic settings.
settings = {}

# Verifies p3 installment.
settings["_isinstalled"] = False
    
# Name of the shell
settings["__name"] = "p3 PoC"
    
# Current shell version
# The version tuple is formatted: major, minor, mini, special, nickname
settings["__version"] = (1, 0, 0, "a1", "Victory")

# Version history
# Lists old version tuples, in chronological order
settings["__version_history"] = [(0, 1, 0, "a1", "RUN"),(0, 1, 0, "a0", "Mainish"),(0, 2, 0, "a1", "Putapininit")]

# Pinned programs
# Contains all shortcuts to run programs.
settings["pinned"] = {}