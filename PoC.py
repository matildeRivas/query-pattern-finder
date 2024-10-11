from typing import List
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import random

sparql = SPARQLWrapper("http://localhost:3030/jena/sparql")
sparql.setReturnFormat(JSON)

query_template = [
    "?x1 <http://www.wikidata.org/prop/direct/{p}> ?x2 ",
    "?x2 <http://www.wikidata.org/prop/direct/{p}> ?x3 ",
    "?x3 <http://www.wikidata.org/prop/direct/{p}> ?x4 ",
    "?x4 <http://www.wikidata.org/prop/direct/{p}> ?x1 ",
    "?x4 <http://www.wikidata.org/prop/direct/{p}> ?x5",
    "?x5 <http://www.wikidata.org/prop/direct/{p}> ?x6 ",
    "?x6 <http://www.wikidata.org/prop/direct/{p}> ?x7 ",
    "?x7 <http://www.wikidata.org/prop/direct/{p}> ?x8 ",
    "?x8 <http://www.wikidata.org/prop/direct/{p}> ?x5 ",
]


def run_query(predicates: List[str]):
    query = [query_template[i].format(p = predicates[i]) for i in range(len(predicates))]
    #print(f"SELECT (COUNT(?x1) as ?results) WHERE {{ {' . '.join(query)} }}")
    sparql.setQuery(f"SELECT (COUNT(?x1) as ?results) WHERE {{ {' . '.join(query)} }}")
    results = sparql.query().convert()
    return int(results['results']['bindings'][0]['results']['value'])


def store_results(predicates: List[str]):
    with open('square_barbell.txt', "a") as file:
        file.write(','.join(predicates) + '\n')


def backtracking(all_predicates, counter,current: List[str]=[]):
    if len(current) == len(query_template):
        store_results(current)
        counter = counter + 1
        print(
            current
        )
        return counter
    
    for p in all_predicates:
        if p not in current:
            new = current + [p]
            results = run_query(new)
            
           # print(f'probando {new}\n\tobtuvo {results} resultados')
            if results > 0:
                counter = backtracking(all_predicates, counter, new)
        if counter > 2000:
            break
    
    return counter

def main():
    with open('filtered_properties_wikidata.csv') as file:
        all_predicates =  file.readline().split(',')
    random.shuffle(all_predicates)
    counter = 0
    backtracking(all_predicates, counter)
    return


main()
