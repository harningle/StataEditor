The package is still at work-in-progress stage. All comments and suggestions are most welcome!


## Reporting issues

If anything does not work as expected, feel free to do not hesitate to [open a new issue](https://github.com/harningle/StataEditor/issues/new/choose) on GitHub. For first time GitHub users, see [here](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue#creating-an-issue-from-a-repository). In your bug report, it's better to have:

* A short and informative title

    :white_check_mark: “twsc” does not trigger scatter plot

    :negative_squared_cross_mark: code snippet working

* A minimal and self-contained code/steps to reproduce the bug

    :white_check_mark: Type “twsc” and press Tab but nothing happens

    :negative_squared_cross_mark: I use scatter plot snippet

* The current outcome

    :white_check_mark: “twsc” + Tab gives “twsc&nbsp;&nbsp;&nbsp;&nbsp;” (twsc with four whitespaces)

    :negative_squared_cross_mark: nothing happens

* The expected outcome

    :white_check_mark: It should trigger `https://github.com/harningle/StataEditor/blob/master/Twoway%20scatter.sublime-snippet` 

    :negative_squared_cross_mark: a scatter plot template

* Log

    :white_check_mark: Press ++ctrl+grave++, and copy the *entire* console log

    :negative_squared_cross_mark: Nothing happens so I have absolutely no idea

* (Potential fix. If you have any idea to fix that, please tell me! You can open an issue and then a pull request)


## Requesting snippets

If you have some frequently used code blocks and want to share with us, please also open an issue, with:

* A concise title as above
* A trigger

    :white_check_mark: Ideally the trigger is “merg”

    :negative_squared_cross_mark: I want a code snippet for merge

* A complete code block

    :white_check_mark: `merge m:1 using "some_data.dta"`

    :negative_squared_cross_mark: It should give us Stata merge command

* The placeholders

    :white_check_mark: In the above code, the “`m`”, “`1`”, and “`some_data.dta`” can be modified

    :negative_squared_cross_mark: I want 1:1, 1:m, and m:1 mode


## General questions

If you have any other questions, just open an issue!
