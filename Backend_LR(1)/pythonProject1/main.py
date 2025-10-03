from grammar_helpers import *
from afd_lr1 import *
from graph_render import *
from derivation_table import *
def test_functions(grammar:str)->None:
    grammar = extend_grammar(grammar)

    print("Gramatica extendida: ")
    print(grammar)
    t, nt = get_terminals_and_non_terminals(grammar)
    print("no terminales: ", nt)
    print("terminales: ", t)
    firsts, follows = get_firsts_and_follows(grammar, t, nt)
    print("firsts: ")
    for c in nt:
        print(f"{c}: {firsts[c]}")
    print("follows: ")
    for c in nt:
        print(f"{c}: {follows[c]}")

def test_afd(grammar:str)->None:
    #extend the grammar
    grammar = extend_grammar(grammar)
    print(grammar)

    #setting variables to make the fsm
    t, nt = get_terminals_and_non_terminals(grammar)
    firsts, follows = get_firsts_and_follows(grammar, t, nt)
    rules=parse_rules(grammar,nt)
    first_rule=rules["S'"][0]
    ancestors=list[AfnNode]()
    afd=list[AfdNode]()

    #creating the fsm
    afn_root=make_afn(rules, nt, firsts, "$", 0, "S'", first_rule, ancestors)
    afd_root=make_afd(afd,{afn_root})

    #render the fsm
    afd_graph=Digraph()
    afn_graph=Digraph()
    create_AFDgraph(afd_root,afd_graph)
    create_AFNgraph(afn_root,afn_graph)
    print("Estados del afd: ",len(afd))
    afd_graph.render("graficos/AFD lr(1)", format="png", view=True)
    afn_graph.render("graficos/AFN lr(1)", format="png", view=True)
def test_table(grammar)->None:
    # extend the grammar
    grammar = extend_grammar(grammar)
    print(grammar)

    # setting variables to make the fsm
    t, nt = get_terminals_and_non_terminals(grammar)
    firsts, follows = get_firsts_and_follows(grammar, t, nt)
    rules = parse_rules(grammar, nt)
    first_rule = rules["S'"][0]
    ancestors = list[AfnNode]()
    afd = list[AfdNode]()

    # creating the fsm
    afn_root = make_afn(rules, nt, firsts, "$", 0, "S'", first_rule, ancestors)
    make_afd(afd, {afn_root})

    table=make_table(afd,t)
    print_table(table,t,nt)


def test_derivation(grammar,string)->None:
    # extend the grammar
    grammar = extend_grammar(grammar)
    print(grammar)

    # setting variables to make the fsm
    t, nt = get_terminals_and_non_terminals(grammar)
    firsts, follows = get_firsts_and_follows(grammar, t, nt)
    rules = parse_rules(grammar, nt)
    first_rule = rules["S'"][0]
    ancestors = list[AfnNode]()
    afd = list[AfdNode]()

    # creating the fsm
    afn_root = make_afn(rules, nt, firsts, "$", 0, "S'", first_rule, ancestors)
    afd_root = make_afd(afd, {afn_root})

    table=make_table(afd,t)
    print_table(table,t,nt)
    accept_rule=grammar.split("\n")[0]
    derivation=derive_string(table,string,accept_rule)
    print("\n")
    print_derivation(derivation,string)






    # n:AfdNode=afd_root.transitions["A"]
    # print(afd.index(n))




grammar1="E -> T E'\nE' -> + T E'\nE' -> ''\nT -> F T'\nT' -> * F T'\nT' -> ''\nF -> ( E )\nF -> id"
grammar2="E -> A + B\nE -> B\nA -> 1\nA -> 2\nA -> ''\nB -> 3\nB -> 4\nB -> ''"
ec_4_g3="S -> a S a\nS -> b S b\nS -> a\nS -> b\nS -> ''"
ec_4_g1="Declaration -> Tipo Var-list\nTipo -> int\nTipo -> float\nVar-list -> id , Var-list\nVar-list -> id"
ec_4_g2="A -> A ( A )\nA -> ''"
ec4_g1_string="float id , id , id"
ec4_g2_string="( ( ) )"

#grammar=str(input("ingrese su gramatica: "))
#test_functions(grammar2)
#test_afd(grammar1)
#test_functions(grammar2)

test_afd(ec_4_g3)
#test_table(ec_4_g2)
#test_derivation(ec_4_g2,ec4_g2_string)





