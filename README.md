Stata Editor for Sublime Text 3/4
=================================

Original work by [Mattias Nordin](http://mattiasnordin.com) and [Sergio Correia](http://scorreia.com/)

<div style="display:flex;">
    <img src="https://raw.githubusercontent.com/harningle/StataEditor/docs/docs/assets/images/use.gif" style="width:45%; height:45%; margin-right:20px;">
    <img src="https://raw.githubusercontent.com/harningle/StataEditor/docs/docs/assets/images/go_to.gif" style="width:45%; height:45%; margin-left:20px;">
</div>


Features
--------

This package enables us to run Stata code from Sublime Text 3/4, with the following features:

* Syntax highlighting
* Code snippets for frequently used commands
* "GoTo Symbol" to navigate through the do files
* And ALL the features coming with Sublime Text and other packages!
* (, which includes Copilot :rofl:)


Installation and Setup
----------------------

This package only works on Windows machines. To install:

1. Install [Sublime Text](https://www.sublimetext.com/) 3 or 4
1. Install [Package Control](https://stackoverflow.com/a/44441455)
1. Add this repository to Package Control
1. Install StataEditor via Package Control
1. Install [pywin32](https://github.com/SublimeText/Pywin32), also via Package Control
1. Change the Stata installation path in user settings

If you are new to Sublime Text, we have a video guide [here](https://github.com/harningle/StataEditor/raw/docs/docs/assets/videos/install.mp4).


Acknowledgments
---------------
The package was originally developed by [Mattias Nordin](http://mattiasnordin.com) and [Sergio Correia](http://scorreia.com/). Thanks to [Adrian Adermon](https://www.adrianadermon.com/) and Daniel Forchheimer for helpful suggestions.


Alternatives
------------

:green_apple: The package only works in Windows. For macOS, try [Stata Enhanced](https://github.com/andrewheiss/SublimeStataEnhanced) or [Stata Improved](https://github.com/zizhongyan/StataImproved)

:atom: [Atom](https://github.com/atom/atom) + [Hydrogen](https://github.com/nteract/hydrogen) + [`stata_kernel`](https://github.com/kylebarron/stata_kernel) is amazing, though GitHub has [sunset](https://github.blog/2022-06-08-sunsetting-atom/) Atom in late 2022

:notebook: If you are a fan of Jupyter Notebook, [`stata_kernel`](https://github.com/kylebarron/stata_kernel) works extremely well

:memo: There are also plugins for vim ([vim-stata](https://github.com/zizhongyan/vim-stata/)) and Emacs ([ado-mode](https://github.com/louabill/ado-mode))