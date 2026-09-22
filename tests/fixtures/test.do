sysuse auto, clear
file open fh using "result.txt", write replace text
file write fh "ok N=`c(N)'" _n
file close fh
