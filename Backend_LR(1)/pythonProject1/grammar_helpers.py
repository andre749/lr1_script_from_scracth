from logging import exception
def extend_grammar(g:str)->str:
    first_char=g.split(" ->")[0]
    return "S' -> "+first_char+"\n"+g

def get_terminals_and_non_terminals(g:str)->(set[str], set[str]):
    terminals:set[str]=set()
    non_terminals:set[str]=set()
    lines=g.split("\n")
    for line in lines:
        rule=line.split(" ->")
        if len(rule)!=2:
            raise exception("not a valid grammar format")
        non_terminals.add(rule[0])
    for line in lines:
        chars=line.split(" ")
        for char in chars:
            if char not in non_terminals and char!="->":
                terminals.add(char)
    terminals.add("$")
    terminals.add("''")
    return terminals,non_terminals

def parse_rules(g:str,nonterminals:set[str])->dict[str,list[list[str]]]:
    lines=g.split("\n")
    rules:dict[str,list[list[str]]]=dict[str,list[list[str]]]()
    for nt in nonterminals:
        rules[nt]=list()
    for line in lines:
        rule=line.split(" -> ")
        rules[rule[0]].append(rule[1].split(" "))
    return rules

def get_firsts_and_follows(g:str,terminals:set[str],nterminals:set[str])->(dict[str,set[str]],dict[str,set[str]]):
    lines=g.split("\n")
    firsts:dict[str,set[str]]={}
    follows:dict[str,set[str]]={}
    for t in terminals:
        firsts[t]=set[str]()
        firsts[t].add(t)

    for nt in nterminals:
        firsts[nt]=set[str]()
        follows[nt]=set[str]()
    #firsts
    changed=True
    while changed:
        changed = False
        for line in lines:

            rule=line.split(" ->")
            chars=rule[1].split(" ")
            epsilon=True
            alpha=rule[0]
            size=len(firsts[alpha])
            i=0
            while epsilon and i<len(chars):
                if chars[i]=='':
                    char="''"
                else:
                    char=chars[i]

                firsts[alpha]=firsts[alpha] | (firsts[char] - {"''"})
                epsilon= "''" in firsts[char]
                i+=1
                if i==len(chars) and epsilon:
                    firsts[alpha].add("''")

            if len(firsts[alpha])!=size:
                changed=True
    #Follows
    follows[lines[0].split(" ->")[0]].add("$")
    for line in lines:
        rule = line.split(" ->")
        chars = rule[1].split(" ")
        i = 0
        while i < len(chars) - 1:
            if chars[i] not in terminals and chars[i] != '':
                follows[chars[i]] = follows[chars[i]] | (firsts[chars[i + 1]] - {"''"})
            i += 1
    changed=True

    while changed:
        changed=False
        for line in lines:
            rule = line.split(" ->")
            alpha = rule[0]
            chars = rule[1].split(" ")
            i = len(chars)-1
            epsilon = True
            while i >= 0 and epsilon and chars[i] not in terminals :
                if chars[i]=='':
                    i -= 1
                    pass
                size=len(follows[chars[i]])
                follows[chars[i]] = follows[chars[i]] | follows[alpha]
                if "''" in firsts[chars[i]]:
                    epsilon = True
                if size!=len(follows[chars[i]]):
                    changed=True
                i -= 1
    return firsts,follows


def print_table(table: list[dict[str, str]], t:set[str], nt:set[str]) -> None:
    print("Tabla de derivacion LR(1): ")

    max_width = max(max(len(c) for c in t|nt)*3,15)
    print( ' '*11, end="")

    for c in t-{"''"}:
        print(f"[{c:^{max_width}}]", end="")
    print(end="||")

    for c in nt:
        print(f"[{c:^{max_width}}]", end="")
    print()
    i=0
    for row in table:
        space=bool(len(str(i))==1)
        print(f"Estado {i}:"," "*space,end="")
        i+=1
        for c in t-{"''"}:
            if c in row.keys():
                print(f"[{row[c]:^{max_width}}]", end="")
            else:
                print(f"[{'':^{max_width}}]", end="")
        print(end="||")

        for c in nt:
            if c in row.keys():
                print(f"[{row[c]:^{max_width}}]", end="")
            else:
                print(f"[{'':^{max_width}}]", end="")
        print()

