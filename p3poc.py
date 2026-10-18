""" --- p3poc.py --- """

# This is the 0th edition of p3, nicknamed 'PoC' for 'proof of concept.'
# This file is the main executable to run the shell/pseudo-OS.

# Import basic modules.
import gint
import ventris.allbase as f

# Show ventris credits.
f.belong2us()

# Import p3 modules.
from p3a.themes import themes
from p3a.ntrfaces import iindex

# For p3sav, and for p3sav only, do we import with *
from p3sav import *

# Flip once.
f.flip()

# Run the main loop.
while True:
  try:
    # If we need to swap interfaces or change theme, do it.
    # Otherwise, run the main loop.
    if vars.get("redirect", False):
      # Set the new interface.
      try:
        iface = iindex[vars["redirect"]](settings, vars, themes)
      except KeyError as exc:
        print("Oops. We tried to access interface '" + str(exc) + "' but didn't find it.")
        raise KeyboardInterrupt()
      
      # Get rid of the redirect.
      vars["redirect"] = None
      
      # Clear temporary variables.
      for var in vars.copy():
        if var.startswith("@"):
          del vars[var]
        
      # Tell us we need to retheme.
      vars["retheme"] = True
      
      # Make sure keypresses don't carry over.
      gint.clearevents()
      
      # Start over.
      continue
    
    elif vars.get("retheme", False):
      # Get rid of the retheme.
      vars["retheme"] = None
      
      # Set the theme.
      iface.settheme()
      
      # Prepare the screen.
      f.clear(themes.gettheme()[0])
      iface.fullblit()
      
      # Start over.
      continue
      
    else:
      # Blit the objects.
      iface.blit()
      
      # Show the screen.
      f.flip()
      
      # Delete what we need for redrawing.
      iface.delete()
    
      # Check key events for variably updated attributes.
      event = gint.pollevent()
      response = iface.respond(event)
      if response == - 1:
        # -1 is the absolute kill switch.
        break
      
      # Update objects.
      iface.update()
  except KeyboardInterrupt:
    break