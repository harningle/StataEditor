import sublime, sublime_plugin
import Pywin32.setup
import win32com.client
import win32api
import os
import re

settings_file = "StataEditor.sublime-settings"


def plugin_loaded():
    global settings
    settings = sublime.load_settings(settings_file)


class VariableCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if view.scope_name(view.sel()[0].a) != 'source.stata ':  # Only work in
            return                                               # do files
        else:
            if settings.get('variable_completions'):  # Get all vars. in the
                try:                                  # current dataset
                    varlist = sublime.stata.VariableNameArray()
                    complist = []
                    for i in varlist:
                        complist.append([i + "\tVariable", i])
                    return complist
                except AttributeError:
                    return
            else:
                return


class FunctionCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if view.scope_name(view.sel()[0].a) != 'source.stata ':
            return
        else:
            if settings.get('function_completions'):
                funclist = [
                    'ceil', 'exp', 'floor', 'int', 'ln', 'log', 'logit', 'max',
                    'min', 'mod', 'round', 'sign', 'sqrt', 'sum', 'Ftail',
                    'invF', 'invFtail', 'normal', 'invnormal', 'poisson',
                    'ttail', 'invt', 'invttail', 'char', 'length', 'lower',
                    'proper', 'real', 'regexm', 'reverse', 'strcat', 'string',
                    'strlen', 'strlower', 'strmatch', 'strpos', 'strproper',
                    'strreverse', 'strtoname', 'strtrim', 'strupper',
                    'subinstr', 'subinword', 'substr', 'trim', 'upper', 'word',
                    'wordcount', 'float', 'inlist', 'inrange', 'matrix',
                    'missing', 'recode', 'return', 'scalar', 'det', 'trace',
                    'cholesky', 'corr', 'diag', 'hadamard', 'inv'
                ]  # Only auto-complete frequently used funcs.
                complist = []
                for i in funclist:
                    complist.append([i + "\tFunction", i + "($1)$0"])
                return complist
            else:
                return


class CommandCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if view.scope_name(view.sel()[0].a) != 'source.stata ':
            return
        else:
            if settings.get("command_completions") == True:
                cmdlist = [
                    "append", "areg", "binreg", "bootstrap", "break", "by",
                    "capture", "char", "chdir", "class", "clear", "cluster",
                    "codebook", "collapse", "compress", "continue", "copy",
                    "correlate", "count", "cross", "describe", "destring",
                    "dfgls", "dfuller", "dir", "display", "do", "duplicates",
                    "dydx", "edit", "egen", "encode", "erase", "error", "estat",
                    "estimates", "estimates_notes", "exit", "export", "factor",
                    "file", "filefilter", "findit", "foreach", "forecast",
                    "format", "forvalues", "generate", "glm", "gmm", "graph",
                    "gsort", "hausman", "heckman", "help", "histogram", "if",
                    "import", "impute", "include", "infile", "infix", "input",
                    "insheet", "ipolate", "isid", "ivreg", "ivregress",
                    "jackknife", "javacall", "joinby", "kdensity", "ksm",
                    "ksmirnov", "label", "levelsof", "lfit", "lincom", "line",
                    "list", "log", "logistic", "logit", "lowess", "lpoly",
                    "lrtest", "macro", "margins", "marginsplot", "mata",
                    "mata_clear", "mata_describe", "mata_drop", "mata_matsave",
                    "mata_memory", "mata_mlib", "mata_mosave", "mata_rename",
                    "mata_which", "matalabel", "matlist", "matrix", "mean",
                    "merge", "mkdir", "mkmat", "mlogit", "newey", "notes",
                    "numlist", "odbc", "ologit", "oprobit", "order", "palette",
                    "pause", "pca", "pcorr", "pctile", "permute", "plot",
                    "plugin", "poisson", "post", "power", "pperron", "predict",
                    "predictnl", "preserve", "probit", "program", "quietly",
                    "range", "recast", "recode", "regress", "rename", "reshape",
                    "return", "rmdir", "save", "scalar", "scatter", "shell",
                    "sleep", "sort", "spearman", "split", "ssc", "statsby",
                    "stfill", "stptime", "streg", "sts", "stset", "stsplit",
                    "stsum", "suest", "sum", "summarize", "sureg", "svy",
                    "svy_estat", "svydescribe", "svygen", "svyset", "svytest",
                    "syntax", "sysdir", "sysuse", "table", "tabstat",
                    "tabulate", "teffects", "test", "testnl", "timer", "tobit",
                    "total", "tsfill", "tsline", "tsset", "ttest", "update",
                    "use", "var", "vce", "webuse", "which", "while", "xpose",
                    "xtdata", "xtdescribe", "xtgls", "xtivreg", "xtline",
                    "xtlogit", "xtreg", "xtset", "xtsum", "xttab", "xttobit",
                    "zip", "reghdfe"]
                complist = []
                for i in cmdlist:
                    complist.append([i + "\tCommand", i])
                return complist
            else:
                return


class FileCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if view.scope_name(view.sel()[0].a) != 'source.stata ':
            return
        else:
            if settings.get("file_completions") != False:
                complist = []
                global_map = {r'^\d*_*[cC]ode/': '\$code/',
                              r'^\d*_*[dD]ata/': '\$data/',
                              r'^\d*_*[rR]awdata/': '\$rawdata/',
                              r'^\d*_*[tT]emp/': '\$temp/',
                              r'^\d*_*[fF]igure/': '\$fig/',
                              r'^\d*_*[tT]able/': '\$tab/'}
                for i in sublime.file_list:
                    for key in global_map:
                        filename = re.sub(key, global_map[key], i)
                    complist.append([i + "\tfile", '"' + filename + '"'])
                return complist
            else:
                return
