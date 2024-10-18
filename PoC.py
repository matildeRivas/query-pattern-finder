from typing import List
from SPARQLWrapper import SPARQLWrapper, JSON
import random

sparql = SPARQLWrapper("http://localhost:3030/jena/sparql")
sparql.setReturnFormat(JSON)

query_template = [
    "?x1 {p} ?x2 ",
    "?x2 {p} ?x3 ",
    "?x3 {p} ?x4 ",
    "?x4 {p} ?x5 ",
    "?x5 {p} ?x1 ",
    "?x5 {p} ?x6 ",
    "?x6 {p} ?x7 ",
    "?x7 {p} ?x8 ",
    "?x8 {p} ?x9 ",
    "?x9 {p} ?x10 ",
    "?x10 {p} ?x6 ",
]


def run_query(predicates: List[str]):
    c = len(predicates)
    n = len(query_template)
    query = [query_template[i].format(p = f'<http://www.wikidata.org/prop/direct/{predicates[i]}>') for i in range(c)]
    query.extend([query_template[i].format(p = f'?p{i}') for i in range(c, n)])

    #for q in query:
     #   print(q)

    #print(f"SELECT (COUNT(?x1) as ?results) WHERE {{ {' . '.join(query)} }}")
    sparql.setQuery(f"SELECT ?x1 WHERE {{ {' . '.join(query)} }} LIMIT 1")
    try:
        results = sparql.query().convert()
        return len(results['results']['bindings'])
    except:
        return 0


def store_results(predicates: List[str]):
    with open('penta_barbell.txt', "a") as file:
        file.write(','.join(predicates) + '\n')


def backtracking(all_predicates,current: List[str]=[]):
    if len(current) == len(query_template):
        store_results(current)
        print(
            current
        )
        return 1
    local_counter = 0
    counter = 0
    for p in all_predicates:
        if p not in current:
            new = current + [p]
            results = run_query(new)

           # print(f'probando {new}\n\tobtuvo {results} resultados')
            if results > 0:
                local_counter += backtracking(all_predicates, new)
        if local_counter > 5:
            if len(current) == 0:
                counter += local_counter
                if counter > 100:
                    break
                local_counter = 0
                continue
            else:
                break

    return local_counter

def main():
    with open('filtered_properties_wikidata.csv') as file:
        all_predicates =  file.readline().split(',')
    random.shuffle(all_predicates)
    backtracking(all_predicates)
    return


main()