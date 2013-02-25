Purpose
=======

Android has a reader app for common unix/linux manpages:

https://play.google.com/store/apps/details?id=com.oscd.manpages&hl=en

It doesn't include everything though.  I wrote this script to add pages for git (so meta...)
and I had been meaning to pick up some python.

Usage
=====

sync-oscd-manpages.py -f <file> -m <man pages> -u 

Arguments
---------

* -f|--file   
  path to manpages sqlite file on the device SD card

* -m|--man
  comma separated list of man pages to add

* -u|--update 
  allow existing pages to be updated.


Disclaimer
==========

This software has not been tested in a very long time.  USE AT YOUR OWN RISK.
