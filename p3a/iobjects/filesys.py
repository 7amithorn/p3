""" --- filesys.py --- """

# Handles classes that interact with the file system.

import builtins
import ventris.allbase as f

DIR_PREF = "#@"
SAVE_F = "p3sav.py"

PATHSEP = "\\"
IMPCHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890"
PATHCHARS = IMPCHARS + "()[]'\"-~" + PATHSEP

class ShutdownD():
  """Handles shutdown."""
  
  def __init__(self):
    """Initialize values."""
    pass
  
  def respond(self, event, settings, vars):
    """Save user info and shut down."""
    lines = self.getlines()
    self.writelines(lines, settings)
    return - 1
  
  def getlines(self):
    """Get the lines from the save file."""
    lines = []
    with open(SAVE_F) as save:
      for line in save:
        lines.append(line)
        if line.strip() == DIR_PREF + "end":
          break
    return lines
  
  def writelines(self, lines, settings):
    """Rewrite the save file."""
    with open(SAVE_F, "w") as save:
      for line in lines:
        save.write(line)
      save.write("\n# Saved settings\n\n")
      for key, value in settings.items():
        if not key.startswith("__"):
          save.write("settings[" + repr(key) + "] = " + repr(value) + "\n")


class PathError(ValueError):
  """Error class for path problems."""
  
  def __init__(self, *args):
    """Initialize values."""
    super().__init__(*args)


class RunD():
  """
  Runs external files.
  Only runs them when self.trigger is true.
  """
  
  def __init__(self, varn="@run", trigger="@exe", err="@err"):
    """Initialize values."""
    self.varn, self.trigger, self.err = varn, trigger, err
  
  def respond(self, event, settings, vars):
    """If able, convert and run the progam in varn."""
    path = vars.get(self.varn, None)
    trigger = vars.get(self.trigger, None)
    if path and trigger:
      self.exe(vars, path)
    
  def exe(self, vars, path):
    """Run a program and associated """
    vars[self.trigger] = False
    vars[self.err] = False
    try:
      pypath = self.convpath(path)
    except PathError as err:
      vars[self.err] = str(err)
    else:
      try:
        err = self.run(pypath)
      except ImportError as err:
        vars[self.err] = str(err)
      else:
        if err:
          vars[self.err] = err
        f.flip() # Restore the screen as the main view.
        vars["retheme"] = True
  
  def run(self, pypath):
    """Run the specified path."""
    try:
      prog = builtins.__import__(pypath)
    except KeyboardInterrupt:
      prog = None
    except ImportError:
      return "File not found"
    except Exception as err:
      return "Program threw " + str(type(err))[8:-2]
    del prog
    
  def convpath(self, path):
    """Convert a given path."""
    if path.startswith(PATHSEP):
      path = path[1:]
    if path.endswith(".py"):
      path = path[:-3]
    for char in path:
      if char not in IMPCHARS + PATHSEP:
        raise PathError(char + " not valid path character")
    splpath = path.split(PATHSEP)
    return ".".join(splpath)

class RunPinnedD(RunD):
  """Run a pinned program."""
  
  def __init__(self, varn="@run", trigger="@exe", err="@err"):
    """Initialize values."""
    super().__init__(varn, trigger, err)
  
  def respond(self, event, settings, vars):
    """Pull out a pin and run it."""
    pin = vars.get(self.varn, None)
    path = settings["pinned"].get(pin, None) if pin else None
    trigger = vars.get(self.trigger, None)
    if path and trigger:
      self.exe(vars, path)
    elif not path and trigger:
      vars[self.err] = "invalid pin"