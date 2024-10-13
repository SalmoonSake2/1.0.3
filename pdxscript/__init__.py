'''
pdxscript.py

This module link pdx(Paradox Interactive) script and python code.

Class
-----------------------------------------------------------------------
- `Statement` : Data Storing Class for pdx script statement. Such as
                scope, effect, and trigger.
- `PDXscript` : Data Storing Class for pdx script. It works as list of 
                Statement objects. And also provide methods to read/write
                pdx script. 
- `ScriptNotClosedException` : Exception Class.
- `ViolatedPathException` : Exception Class.

Usage
-----------------------------------------------------------------------
>>> from hoi4script.pdxscript import PDXscript
>>> path = "C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV/common/national_focus/finland.txt"
>>> script = PDXscript(path)

More
-----------------------------------------------------------------------
- `version` : 1.0.3
- `last update`: 2024.10.10
- `author` : Salmoon Sake
'''

from .pdxscript import Statement
from .pdxscript import PDXscript
from .pdxscript import ScriptNotClosedException
from .pdxscript import ViolatedPathException

__all__ = ["Statement","PDXscript","ScriptNotClosedException","ViolatedPathException"]

__version__ = '1.0.3'