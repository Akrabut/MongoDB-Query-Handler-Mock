import sys # for argv use
import operator # for string to operator conversion
import json # for string to dict conversion


inventory = [
  { "name": "ab", "qty": 15, "price": 2.99 },
  { "name": "cd", "qty": 5, "price": 3.99 },
  { "name": "ij", "qty": 3, "price": 1.99 },
  { "name": "xy", "qty": 20, "price": 1.99 }
]

# call method by string arg
def operate(op, a, b):
    return getattr(operator, op)(a, b)

# handles eq, ne, gt, gte, lt, lte, in and nin
def operator_reducer(op, a, b):
    if op == "lte": return operate("le", a, b)
    if op == "gte": return operate("ge", a, b)
    if op == "in": return operate("contains", a, b)
    if op == "nin": return not operate("contains", a, b)
    return operate(op, a, b)

def values_from_query(query):
    # returns query operator, query property, query value
    return [query.values()[0].keys()[0], query.keys()[0], query.values()[0].values()[0]]

def fit_all_criteria(item, queries):
    for query in queries:
        query_values = values_from_query(query)
        if not operator_reducer(query_values[0], item[query_values[1]], query_values[2]): return False
    return True

def fit_any_criteria(item, queries):
    for query in queries:
        query_values = values_from_query(query)
        if operator_reducer(query_values[0], item[query_values[1]], query_values[2]): return True 
    return False

# handles 'and' and 'or' queries
def relevant_items_complex(prop, queries):
    callback = (fit_all_criteria if prop == "$and" else fit_any_criteria)
    return filter(lambda item: callback(item, queries), inventory)


# given a property, operator and a value, returns an array of items on which the operation returned true
def relevant_items(prop, op, b):
    return filter(lambda item: operator_reducer(op, item[prop], b), inventory)

def main():
    if len(sys.argv) < 2: 
        print("No arguments given")
        return

    # dict string to dict
    operation = json.loads(sys.argv[1])
    prop = operation.keys()[0]
    query = operation.values()[0]
    if prop in ["$and", "$or"]: 
        print(relevant_items_complex(prop, query))
        return

    # handle { something: value } cases as opposed to { something: { operator: value }}
    # query.keys()[0] is the operator, query.values()[0] is the value
    result = relevant_items(prop, query.keys()[0], query.values()[0]) if type(query) is dict else relevant_items(prop, "eq", query)
    print(result)


main()

