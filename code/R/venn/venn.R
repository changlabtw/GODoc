first = "/Users/blueswen/Documents/protein/Supplementary_data/data/SwissProt-t0/id.txt"
second = "/Users/blueswen/Documents/protein/Supplementary_data/data/SwissProt-t1/id.txt"
first = c(readLines(first))
second = c(readLines(second))

both <- first[first %in% second] # in both, same as call: intersect(first, second)
onlyfirst <- first[!first %in% second] # only in 'first', same as: setdiff(first, second)
onlysecond <- second[!second %in% first] # only in 'second', same as: setdiff(second, first)
length(both)
length(onlyfirst)
length(onlysecond)
require("gplots")
venn(list(t0_BPO = first, t1_BPO = second))
