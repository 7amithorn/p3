""" --- objects.py --- """

# Handles objects that do not fall into any other categories.

import ventris.allbase as f
import ventris.gstats as g
import ventris.ntrface as n
import gint

from graphics import ThemedText

dtheme = [(255,255,255)] + ([(0,0,0)] * 4)

class ValidationError(ValueError):
  """Error class for ValidatorText."""
  
  def __init__(self, *args):
    """Initialize values."""
    super().__init__(*args)

class ValidatorText(ThemedText):
  """
  Validates input in vars[self.varn].
  Redirects if everything is valid.
  """
  
  def __init__(self, ul, varn, redirect, lengths=(None, None), functs=None, wlst=None, blst=None, comp=None, errors=None, theme=dtheme):
    """
    Initialize values.
    blst and wlst are character white and blacklists.
    funct is a list of testing functions.
    lengths is a tuple of min and max lengths.
    comp is a tuple indicating what value to compare to.
    """
    super().__init__(ul, "", theme)
    self.varn, self.redirect = varn, redirect
    self.lengths, self.functs, self.wlst, self.blst, self.comp = lengths, functs, wlst, blst, comp
    self.errors = {"short" : "input too short", "long" : "input too long", "funct": "failed validation", "wlst" : "invalid character(s)", "blst" : "invalid character(s)", "comp" : "mismatch with stored value",}
    if errors:
      self.errors.update(errors)
    self.tind = 3
    self.settheme(theme)
  
  def tlen(self, string):
    """Test length."""
    if self.lengths[0]:
      if len(string) < self.lengths[0]:
        raise ValidationError(self.errors["short"])
    if self.lengths[1]:
      if len(string) > self.lengths[1]:
        raise ValidationError(self.errors["long"])
  
  def tfunct(self, string):
    """Apply test functions."""
    if self.functs:
      for fn in self.functs:
        if not fn(string):
          raise ValidationError(self.errors["funct"])
  
  def tlst(self, string):
    """Apply white and blacklists."""
    if self.wlst:
      for ch in string:
        if ch not in self.wlst:
          raise ValidationError(self.errors["wlst"])
    if self.blst:
      for ch in self.blst:
        if ch in string:
          raise ValidationError(self.errors["blst"])
  
  def tcomp(self, string, settings, vars):
    """Compare the string to a value in settings or vars."""
    if self.comp:
      val = (settings if self.comp[0] == "s" else vars).get(self.comp[1], "")
      if string != val:
        raise ValidationError(self.errors["comp"])
  
  def respond(self, event, settings, vars):
    """Validate text, if any."""
    if vars.get(self.varn, False):
      string = vars[self.varn]
      try:
        self.tlen(string)
        self.tlst(string)
        self.tfunct(string)
        self.tcomp(string, settings, vars)
      except ValidationError as err:
        self.change(str(err))
        vars[self.varn] = None
      else:
        self.change("")
        vars["redirect"] = self.redirect

class VarText(ThemedText):
  """Display a value in vars or settings."""
  
  def __init__(self, ul, vos, key, theme=dtheme, label=("","")):
    """
    Initialize values.
    vos holds whether the value should be taken from vars or settings.
    """
    super().__init__(ul, "", theme)
    self.vos = vos if vos in ("v", "s") else "v"
    self.key = key
    self.label = label
  
  def get(self, settings, vars):
    """Get the value needed."""
    return (settings if self.vos == "s" else vars).get(self.key, "")
  
  def respond(self, event, settings, vars):
    """Get the value to show."""
    self.text = self.label[0] + str(self.get(settings, vars)) + self.label[1]


class EmptyText(VarText):
  """Shows a notice if a variable is empty."""
  
  def __init__(self, ul, vos, key, theme=dtheme, label="", tind=1):
    """Initialize values."""
    super().__init__(ul, vos, key, theme, label)
    self.tind = tind
  
  def respond(self, event, settings, vars):
    """See if the object has a value."""
    if self.get(settings, vars):
      self.text = ""
    else:
      self.text = self.label