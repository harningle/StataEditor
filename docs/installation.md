The recommended way to install StataEditor is via [Package Control](https://packagecontrol.io/).


## Install Sublime Text 3/4

First of all, we need Sublime Text installed (and Stata of course). Sublime Text is a text/source code editor with native support for many languages. With plugins, software like Stata also works well in it. To download and install, go to [https://www.sublimetext.com/](https://www.sublimetext.com/). It's recommended to do a complete installation, rather than using a portable version, because the configuration may be easier. It may be downloaded and evaluated for free, however a [license](https://www.sublimehq.com/store/text) must be purchased for continued use.

!!! tip "3 or 4?"

    This plugin works for *both* Sublime Text 3 and 4. [4](https://www.sublimetext.com/download) is the current version, and [3](https://www.sublimetext.com/3) is no longer updated since 2019. I personally prefer Sublime Text 3 slightly due to easier LaTeX and Markdown integration, but either version is OK for StataEditor.

    === "Why 3?"
    
        * [LaTeX plugin](https://github.com/SublimeText/LaTeXTools) works much more smoothly in 3 (see [SublimeText/LaTeXTools#1539](https://github.com/SublimeText/LaTeXTools/issues/1539), [#1531](https://github.com/SublimeText/LaTeXTools/issues/1531), [#1524](https://github.com/SublimeText/LaTeXTools/issues/1524), [#1517](https://github.com/SublimeText/LaTeXTools/issues/1517), and [#1490](https://github.com/SublimeText/LaTeXTools/issues/1490))
        * Some [Markdown plugin](https://github.com/timonwong/OmniMarkupPreviewer) only supports 3

    === "Why 4?"

        * [Significant improvement](https://www.sublimetext.com/3to4) from 3
        * [Copilot plugin](https://github.com/TerminalFi/LSP-copilot) only supports 4

!!! info "Stata version"

    I've personally tested Stata 15, 16, and 17. Earlier versions could be supported but there is no guarantee.


## Install Package Control

Open Sublime Text, and to [install Package Control](https://packagecontrol.io/installation):

1. Open the command palette (++ctrl+shift+p++ on Windows, and StataEditor does *not* support Linux or Mac OS)
1. Type `Install Package Control`, and press ++enter++


## Install StataEditor

1. Open the command palette (++ctrl+shift+p++) again
1. Type `Package Control: Add Repository`, and press ++enter++
1. Type `https://github.com/harningle/StataEditor` in the input box at the bottom of Sublime Text window, and press ++enter++
1. Do step 1 again (++ctrl+shift+p++)
1. Type `Package Control: Install Package`, and press ++enter++. You may have to wait for a few seconds
1. Type `StataEditor` and press ++enter++ to install
1. Do 3-5 again, but this time install `Pywin32`

[Configure](config.md) StataEditor and you are good to go!
