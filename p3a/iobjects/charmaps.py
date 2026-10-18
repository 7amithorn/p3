""" --- charmaps.py --- """

# Holds charmaps for p3.

import gint

# Default charmap, for ThemedInput
DCHARMAP = {
    gint.KEY_XOT : "@^aA",
    gint.KEY_LOG : "#&bB",
    gint.KEY_LN : "(\\cC",
    gint.KEY_SIN : ")|dD",
    gint.KEY_COS : "$%eE",
    gint.KEY_TAN : "'`fF",
    gint.KEY_FRAC : ":;gG",
    gint.KEY_FD : "=_hH",
    gint.KEY_LEFTP : "(|iI",
    gint.KEY_RIGHTP : ")~jJ",
    gint.KEY_COMMA : ",`kK",
    gint.KEY_ARROW : "><lL",
    gint.KEY_7 : "77mM",
    gint.KEY_8 : "88nN",
    gint.KEY_9 : "99oO",
    gint.KEY_4 : "44pP",
    gint.KEY_5 : "55qQ",
    gint.KEY_6 : "66rR",
    gint.KEY_MUL : "*{sS",
    gint.KEY_DIV : "/}tT",
    gint.KEY_1 : "11uU",
    gint.KEY_2 : "22vV",
    gint.KEY_3 : "33wW",
    gint.KEY_ADD : "+[xX",
    gint.KEY_SUB : "-]yY",
    gint.KEY_0 : "00zZ",
    gint.KEY_DOT : ".=  ",
    gint.KEY_EXP : "!?\"'",
    gint.KEY_NEG : "-_#$",
    "funct" : {
      gint.KEY_ACON : "<ac>",
      gint.KEY_DEL : "<del>",
      gint.KEY_EXE : "<exe>",
      gint.KEY_SHIFT : "<shift>",
      gint.KEY_ALPHA : "<alpha>",
      0 : "<null>"
    }
  }

# Optn keymap, for password reentry
_funct = DCHARMAP["funct"].copy()
_funct[gint.KEY_OPTN] = "<optn>"
OPTNCHARMAP = DCHARMAP.copy()
OPTNCHARMAP["funct"] = _funct