from lib.breakword import break_word

def lcss(s1, s2):
   m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
   longest, x_longest = 0, 0
   for x in range(1, 1 + len(s1)):
       for y in range(1, 1 + len(s2)):
           if s1[x - 1] == s2[y - 1]:
               m[x][y] = m[x - 1][y - 1] + 1
               if m[x][y] > longest:
                   longest = m[x][y]
                   x_longest = x
           else:
               m[x][y] = 0
   return s1[x_longest - longest: x_longest]

def edit_dist(s1, s2):
    last = None
    row = list(range(1, len(s2) + 1)) + [0]
    for x in range(len(s1)):
        _, last, row = last, row, [0] * len(s2) + [x + 1]
        for y in range(len(s2)):
            delcost = last[y] + 1
            addcost = row[y - 1] + 1
            subcost = last[y - 1] + (s1[x] != s2[y])
            row[y] = min(delcost, addcost, subcost)
    return row[len(s2) - 1]

def split_half(s):
    return (s[:len(s)//2], s[len(s)//2:])

def clean_digraphs(s):
    return s.replace('th', '\a').replace('ng', '\b').replace('ch', '\v')

def restore_digraphs(s):
    return s.replace('\a', 'th').replace('\b', 'ng').replace('\v', 'ch')

def shipname_naive(a, b):
    return split_half(a)[0] + split_half(b)[1]

def shipname_syl(a,b):
    syla = break_word(a)
    sylb = break_word(b)
    first = syla[0:-1] if len(syla) > 1 else syla
    last = sylb[1:] if len(sylb) > 1 else sylb
    return ''.join(first + last)

def shipname_port(a, b, pivot):
    return pivot.join(a.split(pivot)[:-1]) + pivot + b.split(pivot,1)[1]

def shipname(a, b):
    a, b = map(clean_digraphs,(a,b))
    c1 = lcss(a, b)
    c2 = lcss(b, a)
    on_name_edge = a.rindex(c1) == 0 or a.rindex(c2) == 0 or b.index(c1) == len(b)-len(c1) or b.index(c2) == len(b)-len(c2)
    if len(c1) == 0 or on_name_edge:
        return shipname_syl(restore_digraphs(a), restore_digraphs(b))
    return restore_digraphs(min(
        map(lambda a: shipname_port(*a), [(a,b,c1),(a,b,c2),(b,a,c1),(b,a,c2)]),
        key=lambda s: edit_dist(a,s) + edit_dist(b,s) + (len(a+b) - len(s))
    ))

