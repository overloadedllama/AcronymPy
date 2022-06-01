# AcronymPy

A simple and not very useful command-line program which will help you to track all those boring acronyms and abbreviations that you never remember. 

First start set-up, in directory src/ run
> python setup.py

Then you can start using AcronymPy.
AcronymPy usage is:
> python acronympy.py [command] [parameters]

Some examples:
> python acronympy.py show -s theScope

shows you all records which have theScope as scope.

> python acronympy.py add \*IP Internet_Protocol\** -s ip

adds a record for acronym IP that means Internet_Protocol and is in scope ip.

Python and MySQL are required. Python required packages are installed during setup.
