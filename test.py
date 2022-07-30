import requests
import json

querys = ['66b0f5e33f3c209ab46e40f1b85dcc24b0b5e01c',
'96bcf5850a8fce4fe84bbf8f3a1bd05556cdd28e' '66b0f5e33f3c209ab46e40f1b85dcc24b0b5e01c',
'96bcf5850a8fce4fe84bbf8f3a1bd05556cdd28e', '66b0f5e33f3c209ab46e40f1b85dcc24b0b5e01c',
'96bcf5850a8fce4fe84bbf8f3a1bd05556cdd28e']

a = requests.post("http://localhost:5279", json={"method": "claim_search", "params": {"claim_ids": querys}}).json()


results = a["result"]["items"]

ans = []

def reorder_results(querys,results, query_field = "claim_id"):
    ans = []
    for query in querys:
        for r in results:
            if r[query_field] == query:
                ans.append(r)
    return ans

ans = reorder_results(querys,results)


print(json.dumps(ans, indent=4))

