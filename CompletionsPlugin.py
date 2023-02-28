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
        if view.scope_name(view.sel()[0].a) != 'source.stata ':
            return
        else:
            if settings.get("variable_completions") == True:
                try:
                    varlist = sublime.stata.VariableNameArray()
                    complist = []
                    for i in varlist:
                        complist.append([i + "\tVariable",i])
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
            if settings.get("function_completions") == True:
                funclist = ["ceil","exp","floor","int","ln","log","log10","logit","max","min","mod","round","sign","sqrt","sum","trunc","F","Fden","Ftail","invF","invFtail","nF","nFden","nFtail","normal","normalden","normalden","normalden","invnormal","lnnormal","lnnormalden","lnnormalden","lnnormalden","poisson","poissonp","poissontail","invpoisson","invpoissontail","t","tden","ttail","invt","invttail","nt","ntden","nttail","invnttail","npnt","tukeyprob","invtukeyprob","rbeta","rbinomial","rchi2","rgamma","rhypergeometric","rnbinomial","rnormal","rnormal","rpoisson","rt","abbrev","char","indexnot","itrim","length","lower","proper","real","regexm","regexr","regexs","reverse","rtrim","strcat","strdup","string","string","strlen","strlower","strltrim","strmatch","strofreal","strofreal","strpos","strproper","strreverse","strrtrim","strtoname","strtoname","strtrim","strupper","subinstr","subinword","substr","trim","upper","word","wordcount","autocode","c","chop","clip","cond","e","fileexists","fileread","filereaderror","float","fmtwidth","has_eprop","inlist","inrange","irecode","matrix","mi","missing","r","recode","return","s","scalar","tin","twithin","tin","twithin","colnumb","colsof","det","rownumb","rowsof","trace","cholesky","corr","diag","get","hadamard","I","inv","invsym","J","matuniform","nullmat","sweep","vec","vecdiag"]
                complist = []
                for i in funclist:
                    complist.append([i + "\tFunction",i + "($1)$0"])
                return complist
            else:
                return

class CommandCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if view.scope_name(view.sel()[0].a) != 'source.stata ':
            return
        else:
            if settings.get("command_completions") == True:
                cmdlist = ["append","areg","args","assert","binreg","boot","bootstrap","break","by","ca","capture","cc","cd","centile","cf","char","chdir","ci","class","clear","clist","clogit","cloglog","clonevar","cls","cluster","codebook","collapse","compare","compress","confirm","constraint","continue","copy","correlate","corrgram","count","cox","coxbase","creturn","cross","cumsp","cumul","cusum","db","dbeta","deff","describe","destring","dfgls","dfuller","di_g","dir","dirstats","discard","discrim","display","do","doedit","dotplot","dprobit","drop","ds","dstdize","duplicates","dvech","dydx","edit","egen","encode","eq","erase","ereturn","error","esize","estat","estimates","estimates_notes","exit","expand","expandcl","expoisson","export","expr_query","factor","fcast","fcast_compute","fcast_graph","fdasave","file","filefilter","fillin","findfile","findit","fit","for","foreach","forecast","format","forvalues","fp","generate","genrank","gettoken","glm","glogit","gmm","gphdot","gphprint","gprefs","graph","graph7","grebar","greigen","grmeanby","gs_fileinfo","gs_filetype","gs_graphinfo","gs_stat","gsort","h","hadimvo","hausman","haver","heckman","heckoprobit","heckprobit","help","hetprobit","histogram","hotel","if","import","import_delimited","import_excel","import_haver","impute","include","infile","infix","input","insheet","inspect","inten","intreg","ipolate","ir","irf","irf_create","is_svy","isid","ivpoisson","ivprobit","ivreg","ivregress","ivtobit","jackknife","javacall","jkstat","joinby","kappa","kdensity","ksm","ksmirnov","kwallis","label","labelbook","ladder","levels","levelsof","leverage","lfit","lincom","line","linktest","list","log","logistic","logit","lookfor","lookup","lowess","lpoly","lrecomp","lroc","lrtest","lsens","lstat","ltable","lv","macro","makecns","manova","margins","marginsplot","mark","mata","mata_clear","mata_describe","mata_drop","mata_matsave","mata_memory","mata_mlib","mata_mosave","mata_rename","mata_which","matalabel","matlist","matrix","mca","mcc","mds","mdslong","mdsmat","mdytoe","mean","means","memory","merge","merge_10","mfx","mi","mixed","mkdir","mkmat","ml","ml_hold","ml_score","mlogit","more","nbreg","net","newey","notes","numlist","odbc","ologit","ologitp","oneway","oprobit","opts_exclusive","order","orthog","outfile","outsheet","ovtest","palette","parse","parse_dissim","pause","pca","pcorr","pctile","pergram","permute","plot","plugin","poisgof","poisson","post","power","pperron","predict","predictnl","preserve","print","probit","profiler","program","proportion","prtest","psdensity","putexcel","putmata","pwcompare","pwmean","qby","qreg","quadchk","query","quietly","range","ranksum","ratio","rcof","recast","recode","reg3","regress","remap","rename","renpfix","repeat","reshape","return","rmdir","roccomp","rocfit","rocreg","rocregplot","roctab","rolling","rologit","rotate","rotatemat","rreg","runtest","sample","sampsi","save","scalar","scatter","scobit","score","scoreplot","screeplot","sdtest","search","separate","serrbar","serset","set_defaults","shell","signestimationsample","signrank","simulate","sktest","sleep","slogit","smooth","snapshot","sort","spearman","split","ssc","ssd","sspace","st","st_is","stack","statsby","stbase","stci","stcox","stcrreg","stcstat","stcurve","stem","stfill","stptime","strate","streg","sts","stset","stsplit","stsum","suest","sum","summarize","sureg","svar","svy","svy_estat","svydescribe","svygen","svymarkout","svymlog","svyopts","svyset","svytest","symmetry","syntax","sysdir","sysuse","tabdisp","table","tabstat","tabulate","teffects","test","testnl","teststd","tetrachoric","timer","tobit","tokenize","total","tpoisson","translate","tsfill","tsline","tsset","tssmooth","ttest","tutorial","twoway__function_gen","twoway__histogram_gen","twoway__kdensity_gen","type","update","use","var","vce","vec","version","view","webdescribe","webseek","webuse","which","while","xcorr","xi","xmlsave","xpose","xtcorr","xtdata","xtdescribe","xtgls","xtintreg","xtivreg","xtline","xtlogit","xtreg","xtset","xtsum","xttab","xttobit","zip","zipfile"]
                complist = []
                for i in cmdlist:
                    complist.append([i + "\tCommand",i])
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
