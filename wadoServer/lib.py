#!/usr/bin/python
# -*- coding: utf-8 -*-


import commands

class CmdException(Exception):
    """Exception representing a command line error"""
    pass

def trycmd(cmd):
    """Try to execute the given command, raising an Exception on errors"""
    (exitstatus, outtext) = commands.getstatusoutput(cmd)
    if exitstatus != 0:
        raise CmdException, "cmd: %s\noutput: %s" % (cmd, outtext)