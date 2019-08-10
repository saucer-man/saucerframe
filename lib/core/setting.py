#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""
import sys
import os

GIT_REPOSITORY = "https://github.com/saucer-man/saucerframe"
WEBSITE = "https://saucer-man.com"
BANNER = r"""
                               __  {website}                         
                              / |                         
___  __ _ _   _  ___ ___ _ ___| | _ __ __ _ _ __ ___   ___ 
/ __|/ _` | | | |/ __/ _ \ '__|  _| '__/ _` | '_ ` _ \ / _ \
\__ \ (_| | |_| | (_|  __/ |  | | | | | (_| | | | | | |  __/
|___/\__,_|\__,_|\___\___|_|  |_| |_|  \__,_|_| |_| |_|\___|                                                                                                
""".format(website=WEBSITE)

version = 1.0

IS_WIN = True if (sys.platform in ["win32", "cygwin"] or os.name == "nt") else False