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

<video width="80%" height="80%" controls>
    <source src="../assets/videos/demo.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

