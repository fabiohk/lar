from collections import defaultdict

def matchingStrings(stringList: list[str], queries: list[str]) -> list[int]:
    strings_count_map = defaultdict(int)
    for string in stringList:
        strings_count_map[string] += 1
        
    return [strings_count_map[query] for query in queries]

def naive_matchingStrings(stringList, queries):
    return [count_matches(query, stringList) for query in queries]

def count_matches(query: str, stringList: list[str]) -> int:
    count = 0
    for string in stringList:
        if string == query:
            count += 1
    return count