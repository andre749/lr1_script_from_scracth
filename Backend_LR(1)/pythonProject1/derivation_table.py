

from pythonProject1.afd_lr1 import AfdNode

def node_to_row(afd:list[AfdNode], node:AfdNode, t:set[str])-> dict[str:str]:
    row:dict[str:str]=dict()
    rules=node.rules
    for rule in rules:
        shift_token=rule.get_shift_token()
        if shift_token is None:
            r=rule.to_str_without_st()
            if rule.search_token in row.keys() and r!=row[rule.search_token]:

                return {"": "Grammar is not Lr1"}
            row[rule.search_token]=r

        elif shift_token in t:
            r='s'+str(afd.index(node.transitions[shift_token]))
            if shift_token in row.keys() and r!= row[shift_token]:

                return {"": "Grammar is not Lr1"}
            row[shift_token]=r
        else:
            r= str(afd.index(node.transitions[shift_token]))

            if shift_token in row.keys() and r!= row[shift_token]:

                return {"": "Grammar is not Lr1"}
            row[shift_token] = r
    return row



def make_table(afd:list[AfdNode],terminals:set[str]):
    table=list[dict[str:str]]()
    for state in afd:
        row=node_to_row(afd, state, terminals)
        if row=={"":"Grammar is not Lr1"}:
            return [{"":"Grammar is not Lr1"}]
        table.append(row)
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
    valid=True
    invalid_message="Cadena invalida para la gramatica"

    while rule!=accept_rule and valid:
        derivation.append(DerivationRow(stack.copy(), chars.copy(), rule))
        length=len(stack)
        last_state=stack[length-1]
        if not isinstance(last_state,int):
            last_state = stack[length - 2]
            if stack[length-1] not in table[last_state].keys():
                valid=False
                rule=invalid_message
            else:
                rule=table[last_state][stack[length-1]]
        else:
            if chars[0] not in table[last_state].keys():
                valid=False
                rule=invalid_message
            else:
                rule = table[last_state][chars[0]]
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
            if rule!=invalid_message:
                stack.append(base)


    return derivation


def print_derivation(derivation:list[DerivationRow],s)->None:
    invalid_message="Cadena invalida para la gramatica"
    max_width=0
    for st in derivation[0].input:
        max_width+=len(st)
    max_width*=5
    print("derivacion lr(1) de: "+s)
    print(" "*9+"[stack:"+" "*(max_width-6)+"]" + "[input:"+" "*(max_width-6)+"]"+"[rule:"+" "*(max_width-5)+"]")
    i=1
    for paso in derivation:
        size=len(str(i))
        print(f"Paso {i}:" +" "*(3-size),end="")
        i+=1
        paso.print(max_width)
    if derivation[len(derivation)-1].rule!=invalid_message:
        print("Cadena aceptada")



