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

def lo_quiero_todo(grammar:str, string:str= "", graph:bool=False)->None:
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

    if graph:
        afd_graph = Digraph()
        afn_graph = Digraph()
        create_AFDgraph(afd_root,afd_graph)
        create_AFNgraph(afn_root,afn_graph)
        afd_graph.render("graficos/AFD lr(1)", format="png", view=True)
        afn_graph.render("graficos/AFN lr(1)", format="png", view=True)

    print("Estados del afd: ",len(afd))
    table=make_table(afd,t)
    if table==[{"":"Grammar is not Lr1"}]:
            print(table[0][""])
            return
    print_table(table,t,nt)

    if string!="":
        accept_rule=grammar.split("\n")[0]
        derivation=derive_string(table,string,accept_rule)
        print("\n")
        print_derivation(derivation,string)



C="E -> T E'\nE' -> + T E'\nE' -> ''\nT -> F T'\nT' -> * F T'\nT' -> ''\nF -> ( E )\nF -> id"
grammar2="E -> A + B\nE -> B\nA -> 1\nA -> 2\nA -> ''\nB -> 3\nB -> 4\nB -> ''"
ec_4_g3="S -> a S a\nS -> b S b\nS -> a\nS -> b\nS -> ''"
ec_4_g1="Declaration -> Tipo Var-list\nTipo -> int\nTipo -> float\nVar-list -> id , Var-list\nVar-list -> id"
ec_4_g2="A -> A ( A )\nA -> ''"
ambiguous_grammar="A -> B\nA -> C\nB -> xd\nC -> xd"
grammar3="e -> e + n\ne -> n"
ec4_g1_string="float id , id , id"
ec4_g2_string="( ( ) ( ) ) ( )"
grammar2_string="2 + 3"
grammar3_string="n + n + n + n + n"

bool_arithmetic="e -> ( e )\ne -> e or e\ne -> e and e\ne -> n\nn -> 0\nn -> 1"
bool_funct="0 and 1 or 1 and 0"


lo_quiero_todo(bool_arithmetic)





