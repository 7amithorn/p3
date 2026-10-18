""" --- auxf.py --- """

# Defines auxiliary functions for other modules.

def namegen(name, nlst):
  """Generate an unique name."""
  if name in nlst:
    nname, counter = name, 1
    while nname in nlst:
      counter += 1
      nname = name + str(counter)
  else:
    return name

def lbreak(lst, blen):
  """Break a list into blen width segments."""
  bind, blst = 0, [[]]
  for item in lst:
    bind += 1
    blst[- 1].append(item)
    if bind == blen:
      blst.append([])
      bind = 0
  if blst[- 1] == []:
    blst = blst[:- 1]
  return blst