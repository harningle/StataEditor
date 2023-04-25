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
| ++ctrl+r++ | Goto symbol. A panel will appear where you can navigate through different code sections |
| Code snippet trigger<span class="keys"><span>+</span><kbd class="key-tab">Tab</kbd></span> | Use code snippet. See the builtin snippets below |


## Code snippets

A code snippet is a reusable code block. Below we've listed the trigger and snippet for each of the built-in snippets. To fill in the blank placeholders enclosed in `<>`, simply press ++tab++ while in the snippet.

=== "Loop"

    `fore`:

    ```stata
    foreach w in <varlist> {
        <>
    }
    ```

    `forv`:

    ```stata
    forvalues i = <1>(<1>)<n> {
        <>
    }
    ```

=== "Code block title"

    `hd`:

    ```stata
    /* <Title> ********************************************************************/
    ```

    `hdd`:

    ```stata
    *------------------------------------------------------------------------------*
    * <Title>                                                                      *
    *------------------------------------------------------------------------------*
    ```

    `hd`:

    ```stata
    *------------------------------------------------------------------------------*
    *-------                                                                -------*
    *-------                       STEP <1>. <TITLE>                        -------*
    *-------                                                                -------*
    *------------------------------------------------------------------------------*
    ```


## Video demo

Below is a video demo for summary statistics, scatter plot, and regression.

<div style="position: relative; width: 100%; padding-bottom: 56.25%;">
    <iframe src="https://harning-my.sharepoint.com/personal/wangxy_harning_onmicrosoft_com/_layouts/15/embed.aspx?UniqueId=2537d2fc-e833-42dc-842a-58a7087f5b7b&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=OneUpFileViewer&referrerScenario=EmbedDialog.Create" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" scrolling="no" allowfullscreen title="Demo"></iframe>
</div>
