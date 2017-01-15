def parts(t, p, head=(), tail=tuple(range(1,10))):
    print(t,p,head,tail)
    if t == 0 and p == 0:
        return [tuple(sorted(head))]
    if t < 0 or len(tail) == 0:
        return []
    first = tail[0]
    rest = tail[1:]
    return parts(t-first, p-1, head+(first,), rest) + parts(t, p, head, rest)

def partswith(t, p, inc, exc):
    head = inc
    tail = tuple([i for i in list(range(1,10)) if i not in inc+exc])
    return parts(t-sum(inc), p-len(inc), head, tail)

print(parts(12,5))
