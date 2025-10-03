
from pythonProject1.afd_lr1 import AfdNode

def turn_afd_into_row(afd:list[AfdNode],node:AfdNode,t:set[str])->dict[str:str]:
    row=dict[str:str]()
    rules=node.rules
    for rule in rules:
        shift_token=rule.get_shift_token()
        if shift_token is None:
            row[rule.search_token]=rule.to_str_without_st()

        elif shift_token in t:
            row[shift_token]='s'+str(afd.index(node.transitions[shift_token]))
        else:
            row[shift_token] = str(afd.index(node.transitions[shift_token]))
    return row


def make_table(afd:list[AfdNode],terminals:set[str]):
    table=list[dict[str:str]]()
    for state in afd:
        table.append(turn_afd_into_row(afd,state,terminals))
    return  table

class DerivationRow:
    def __init__(self,stack:list[str|int],input:list[str],rule:str):
        self.stack:list[str|int]=stack
        self.input:list[str]=input
        self.rule:str=rule
    def print(self,max_width:int) ->None:
        s=""
        for i in self.stack:
            s+=str(i)+" "
        inp=""
        for i in self.input:
            inp+=i+" "
        print(f"[{s:^{max_width}}]",end="")
        print(f"[{inp:^{max_width}}]",end="")
        print(f"[{self.rule:^{max_width}}]")


def derive_string(table:list[dict[str:str]], s:str, accept_rule)->list[DerivationRow]:
    stack:list[str|int]=[0]
    chars=s.split(" ")
    chars.append("$")
    rule=""
    derivation=list[DerivationRow]()
    while rule!=accept_rule:
        length=len(stack)
        last_item=stack[length-1]
        if not isinstance(last_item,int):
            last_item = stack[length - 2]
            rule=table[last_item][stack[length-1]]
        else:
            rule=table[last_item][chars[0]]
        if "->" not in rule and rule[0]=="s":
            stack.append(chars.pop(0))
            stack.append(int(rule[1:]))
        elif rule.isdigit():
            stack.append(int(rule))
        else:   #reduction
            rule_=rule.split(" -> ")
            base=rule_[0]
            if len(rule_)==1:
                body=[]
                base=rule.split(" ")[0]
            else:
                body=rule_[1].split(" ")
                body.reverse()
            top_chunk=list[str]()
            while top_chunk!=body and len(stack):
                top=stack.pop(length-1)
                length-=1
                if not isinstance(top, int):
                    top_chunk.append(top)
            stack.append(base)
        derivation.append(DerivationRow(stack.copy(), chars.copy(), rule))
    return derivation


def print_derivation(derivation:list[DerivationRow],s)->None:

    max_width=0
    for st in derivation[0].input:
        max_width+=len(st)
    max_width*=5
    print("derivacion lr(1) de: "+s)
    print(" "*9+"[stack:"+" "*(max_width-6)+"]" + "[input:"+" "*(max_width-6)+"]"+"[rule:"+" "*(max_width-5)+"]")
    i=0
    for paso in derivation:
        size=len(str(i))
        print(f"Paso {i}:" +" "*(3-size),end="")
        i+=1
        paso.print(max_width)



