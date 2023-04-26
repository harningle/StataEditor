Below are the keyboard shortcuts and code snippets that come with this plugin. 


## Keyboard shortcuts

<style>
    th {
        border: 0.5px solid #0000001f;
        border-right: none;
        border-left: none;
        border-bottom: 1px solid;
        border-bottom-color: #4051B5;
    }
</style>


| Shortcut | Description |
| -------- | ----------- |
| Nothing selected, ++ctrl+d++ | Run the entire do file |
| Some lines/characters selected, ++ctrl+d++ | Run the selected lines only. If any part of the line is selected, the entire line is included |
| ++ctrl+r++ | [Goto Symbol](https://docs.sublimetext.io/guide/usage/file-management/navigation.html). A panel will appear where you can navigate through different code sections within the do file |
| Code snippet trigger<span class="keys"><span>+</span><kbd class="key-tab">Tab</kbd></span> | Use code snippet |


## Code snippets

A code snippet is a reusable code block. You can find all snippets in Sublime Text > Tools > Snippets. For example, to use the snippet for `-forvalues-`, type `forv` and press ++tab++, and you will see

```stata
forvalues i = 1(1)n {
    
}
```

The cursor now selects the start index `1`. To change it, simply type in the desired number. Then press ++tab++, and the cursor will jump to the `1` inside the parenthesis, where you can change the step size. Press ++tab++ again to move the cursor to `n`, where you can specify the end index. Finally, press ++tab++ one last time to jump inside the curly brackets for the main loop body. This entire process can be completed without using a mouse or arrow keys!


## Auto-completion

The package comes with variable, command, function, and filename auto-completion. All of them support fuzzy match. **Variable** refers to all variables in the `.dta` file we currently open. **Command** and **function** find stuff like `-log-`, `-clear-`, `-logit-`, etc.

!!! bug "Imperfect fuzzy match"

    Sublime Text's fuzzy match algorithm (and in fact the entire Sublime Text) is [not open source](https://forum.sublimetext.com/t/make-sublime-text-open-source/55410/3). So it may not work as you expected. My personal experience is to fuzzy match “sequentially”. E.g. to match “auto-completion”, it's fine to type “atpn”, since “t” is after “a”, “p” is after “t”, and so on. However, if you type “apcu”, though all of the four letters are in the word, Sublime Text is not able to find “auto-completion” for you. That being said, in most cases, however you type it, Sublime Text can always find the word for you!

    If you are interested in the implementation of fuzzy match algorithm, here is [a wonder blog](https://www.forrestthewoods.com/blog/reverse_engineering_sublime_texts_fuzzy_match/) to reverse engineer Sublime Text's fuzzy match. Moreover, [tajmone/fuzzy-search](https://github.com/tajmone/fuzzy-search) collects a set of useful fuzzy search algorithm.

**Filename** auto-completion is slightly more complicated. In the initial folder and all subfolders, the package recursively gets all files with certain extensions, and save their path in a list, when you establish the initial Stata connection from Sublime Text. Then, during your coding, it turns to the list and do (fuzzy) completion for you.

!!!info "Detailed explanation"

    === "Best practice: root directory as the “*initial*” folder"
    
        The “initial” folder refers to the directory containing the do file where you run the initial line(s). In the example project folder structure below, suppose you open `some_code.do` and run the first lines there, the file auto-completion will only suggest files located within `code folder`, and files like `something.docs` will not appear in the list. 
    
        ```
        root directory
        │
        ├── something.docs
        ├── main_do_file.do
        │
        ├── data folder
        │   │
        │   ├── your_data.dta
        │   └── a sub data folder
        │       │
        │       ├── data_a.xlsx
        │       └── data_b.xlsx
        │   
        └── code folder
            │
            └── some_code.do
        ```
    
    === "Only include *extensions* you need"
    
        The file list contains all files with certain extensions. You may want all `.dta` files, all `.xlsx` spreadsheets, and so forth. But it's less likely that your code involves `.docs`. You can change the extensions in Sublime Text > Preferences > Package Settings > StataEditor > [Settings – User](config.md#configure-stataeditor). You can add/delete extensions in `file_completions`. For example, to include `.exe` and `.rtf`, your setting file looks like:
    
        ```
        {
        "ensure_newline_at_eof_on_save": true,
            "stata_path": "C:/Program Files/Stata18/StataMP-64.exe",
            "stata_version": 18,
            "character_encoding": "utf-8",
            "variable_completions": true,
            "function_completions": true,
            "command_completions": true,
            "default_path": "current_path",
            "file_completions": "exe, rtf",
            "waiting_time": 0.5
        }
        ```
        
    === "*Path* are relative to *initial* folder"
        
        The auto-completed path will be relative to your *initial* folder. To illustrate it, we use the same example folder structure. If the initial Stata connection is established when running `main_do_file.do`, then the auto-completed path for `data_a.xlsx` will be `data folder/a sub data folder/data_a.xlsx`.
       
        ```
        root directory
        │
        ├── something.docs
        ├── main_do_file.do
        │
        ├── data folder
        │   │
        │   ├── your_data.dta
        │   └── a sub data folder
        │       │
        │       ├── data_a.xlsx
        │       └── data_b.xlsx
        │   
        └── code folder
            │
            └── some_code.do
        ```
    
    === "Snippets overrules"
        
        Code snippets has the highest priority. Suppose you have a variable called <code><b>for</b>gi<b>v</b>e</code>, a command called <code>-<b>forv</b>alues-</code>, a file called <code><b>for</b>e<b>v</b>er.csv</code>, and the built-in <code><b>forv</b></code> code snippet. The <code><b>forv</b></code> code snippet will pop up when you type “forv” and press ++tab++. So to match the file <code><b>for</b>e<b>v</b>er.csv</code>, you may type something like `fve`, which avoids <code><b>forv</b></code> snippet trigger.


!!! bug "Memory leak"

    As you can imagine, if your folder has hundreds of thousands of files, it can be slow and lead to [memory leak](https://github.com/mattiasnordin/StataEditor/blob/cf4060920c23df9b0b275aee48a13237a93d7fc8/StataEditor.sublime-settings#L50). My personal experience is, as long as the number of files is at the level of thousands, it works efficiently without any issues.

!!! bug "When you establish the “*initial*” Stata connection"

    One shortcoming is that the file list never gets updated, unless you shutdown Sublime Text and Stata, and re-open them. For example, if you've opened Stata, run a few lines, and created a new `.dta`. This new `.dta` will *not* appear in the file auto-completion list, until you launch Sublime Text again.

    I'm working on this. Suggestions welcome!


## Video demo

Below is a video demo for summary statistics, scatter plot, and regression.

<div style="position: relative; width: 100%; padding-bottom: 56.25%;">
    <iframe src="https://harning-my.sharepoint.com/personal/wangxy_harning_onmicrosoft_com/_layouts/15/embed.aspx?UniqueId=2537d2fc-e833-42dc-842a-58a7087f5b7b&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=OneUpFileViewer&referrerScenario=EmbedDialog.Create" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" scrolling="no" allowfullscreen title="Demo"></iframe>
</div>
