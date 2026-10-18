""" --- _parse.py --- """

# Private module that parses input before doing stuff with it.

def argparse(args):
  """
  Parse an argument string into a usable format.
  A non-regex implementation of argparse's parsing.
  """
  arglist = args.split()
  if arglist:
    parsed = {"command" : arglist.pop(0), "short" : [], "long" : [], "word" : []}
  else:
    return None
  for arg in arglist:
    if arg:
      if arg[:2] == "--":
        parsed["long"].append(arg[2:])
      elif arg[0] == "-":
        if len(arg) > 1:
          for char in arg[1:]:
            parsed["short"].append(char)
        else:
          parsed["short"].append("")
      else:
        parsed["word"].append(arg)
  return parsed