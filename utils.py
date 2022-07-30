def safeget(dic, keys:[], placeholder = None):
    for k in keys:
        try:
            dic = dic[k]
        except KeyError:
            return placeholder
    return dic

def reorder_results(querys,results, query_field = "claim_id"):
    ans = []
    for query in querys:
        for r in results:
            if r[query_field] == query:
                ans.append(r)
    return ans



