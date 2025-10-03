from logging import exception



class NodeRule:
    def __init__(self, base: str, body: list[str], search_token: str):
        self.base = base
        self.body = body
        self.search_token = search_token

    def to_string(self)->str:
        s = self.base + " -> "
        for char in self.body:
            s += char + " "
        s += ", " + self.search_token
        return s
    def is_same(self,other)->bool:
        return self.base==other.base and self.body==other.body and self.search_token==other.search_token

    def get_shift_token(self)->str|None:
        index=self.body.index(".")
        if index+1==len(self.body):
            return None
        return self.body[index+1]

    def to_str_without_st(self)->str:
        s = self.base + " ->"
        for char in self.body:
            if char!=".":
                s+=" "+ char
        return s




class AfnNode:
    def __init__(self, base: str, body: list[str], search_token: str):
        self.rule=NodeRule(base,body,search_token)
        self.epsilon_transitions = []
        self.child = None
        self.shift_token = None

    def add_epsilon(self, node):
        if not isinstance(node, AfnNode):
            raise exception("type must be afn_node")
        self.epsilon_transitions.append(node)

    def add_child(self, token, node):
        if not isinstance(node, AfnNode) and node is not None:
            raise exception("type must be afn_node")
        self.shift_token = token
        self.child = node
    def print(self):
        print(self.get_rule(),end="")

    def get_rule(self)->str:
        return self.rule.to_string()

    def epsilon_clossure(self,epsilon_set:set):
        if self in epsilon_set:
            return

        epsilon_set.add(self)

        for n in self.epsilon_transitions:
            n.epsilon_clossure(epsilon_set)




def make_afn(rules, non_t, firsts,
             search_token:str, dot_index:int, base:str="", rule:list[str]=list[str],
             ancestors_list:list[AfnNode]=list[AfnNode])-> AfnNode | None:

    if dot_index>len(rule):
        return None

    if ["''"]==rule:
        rule=[]

    if dot_index==0:
        for ancestor in ancestors_list:
            a_rule=ancestor.rule.body.copy() #regla del ancestro sin el punto
            a_rule.pop(0)
            if ancestor.rule.search_token==search_token and a_rule==rule and ancestor.rule.base==base :
                return ancestor



    rule_with_dot=rule.copy()
    rule_with_dot.insert(dot_index,".")
    node=AfnNode(base, rule_with_dot, search_token)
    if dot_index == 0:
        ancestors_list.append(node)

    if dot_index>=len(rule) :
        shift_token=None
    else:
        shift_token=rule[dot_index]
    node.add_child(shift_token,
                   make_afn(rules, non_t, firsts, search_token, dot_index + 1, base, rule, ancestors_list)
                   )

    if shift_token in non_t:
        rule_with_st=rule.copy()
        rule_with_st.append(search_token)
        epsilon=True
        i=dot_index+1
        while epsilon:
            next_char = rule_with_st[i]
            epsilon= "''" in firsts[next_char]
            for f in (firsts[next_char]-{"''"}):
                for current_rule in rules[shift_token]:
                    current_node=make_afn(rules, non_t, firsts,
                                          f, 0, shift_token, current_rule, ancestors_list)
                    node.add_epsilon(current_node)
            i+=1

    return node

def print_ancestors(ancestors:list[AfnNode]):
    for a in ancestors:
        node=a
        while node is not None:
            node.print()
            print(f" ({node.shift_token}->) ", end="")
            node = node.child
        print()





class AfdNode:
    def __init__(self,afns:set[AfnNode]):
        self.rules:list[NodeRule]=[]
        self.transitions:dict[str,AfdNode|None]=dict[str,AfdNode]()
        for afn in afns:
            self.rules.append(afn.rule)

    def add_transition(self,shift_token:str,node):
        self.transitions[shift_token]=node

    def get_rules(self)->str:
        s=""
        for rule in self.rules:
            s+=rule.to_string()+"\n"
        return s


def make_afd(afd:list[AfdNode],afns:set[AfnNode])->AfdNode:
    clossure:set[AfnNode]=set()
    for afn in afns:
        afn.epsilon_clossure(clossure)
    node=AfdNode(clossure)

    for n in afd:
        already_exists = True
        if len(n.rules)==len(node.rules):
            for i in range(len(n.rules)):
                already_exists=already_exists and n.rules[i].is_same(node.rules[i])
        else:
            already_exists=False

        if already_exists:
            return n

    afd.append(node)


    transition_chars:set[str]=set()
    for afn in clossure:
        if afn.shift_token is not None:
            transition_chars.add(afn.shift_token)

    for char in transition_chars:
        transition_afns:set[AfnNode]=set()
        for afn in clossure:
            if afn.shift_token==char:
                transition_afns.add(afn.child)
        node.add_transition(char,make_afd(afd,transition_afns))



    return node









