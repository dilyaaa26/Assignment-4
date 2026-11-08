import sys
import json

def solve_ping(data):
    return {"status": "ready"}

def solve_lcs(data):
    s1 = data.get("a", "")
    s2 = data.get("b", "")
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    i, j = n, m
    lcs_chars = []
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            lcs_chars.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    seq = "".join(reversed(lcs_chars))
    return {"length": dp[n][m], "sequence": seq}

def solve_merge(data):
    sizes = data.get("sizes", [])
    n = len(sizes)
    if n <= 1:
        return {"cost": 0, "plan": []}

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i+1] = pref[i] + sizes[i]
    def range_sum(i, j):
        return pref[j+1] - pref[i]

    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + range_sum(i, j)
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k

    plan = []
    def build_plan(i, j):
        if i == j:
            return (i, i)
        k = split[i][j]
        left_res = build_plan(i, k)
        right_res = build_plan(k+1, j)
        plan.append([left_res[0], left_res[1], right_res[1]])
        return (left_res[0], right_res[1])

    build_plan(0, n - 1)
    return {"cost": int(dp[0][n-1]), "plan": plan}

def solve_tree(data):
    n = data.get("n", 0)
    weights = data.get("weights", [])
    edges = data.get("edges", [])

    if n == 0:
        return {"weight": 0, "selected": []}

    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    parent = [-1] * n
    order = []
    stack = [0]
    visited = [False] * n
    visited[0] = True

    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)

    dp0 = [0] * n
    dp1 = [0] * n
    include = [[] for _ in range(n)]
    exclude = [[] for _ in range(n)]

    for u in reversed(order):
        dp1[u] = weights[u]
        include[u] = [u]
        exclude[u] = []

        for v in adj[u]:
            if v != parent[u]:
                if dp0[v] >= dp1[v]:
                    dp0[u] += dp0[v]
                    exclude[u].extend(exclude[v])
                else:
                    dp0[u] += dp1[v]
                    exclude[u].extend(include[v])

                dp1[u] += dp0[v]
                include[u].extend(exclude[v])

    if dp1[0] >= dp0[0]:
        return {"weight": dp1[0], "selected": sorted(include[0])}
    else:
        return {"weight": dp0[0], "selected": sorted(exclude[0])}

def solve_search(data, method):
    text = data.get("text", "")
    pattern = data.get("pattern", "")
    if pattern == "":
        return {"positions": list(range(len(text) + 1))}
    positions = []
    if pattern and text:
        p_len = len(pattern)
        t_len = len(text)
        for i in range(t_len - p_len + 1):
            if text[i:i+p_len] == pattern:
                positions.append(i)
    return {"positions": positions}

def solve_suffix(data):
    text = data.get("text", "")
    n = len(text)
    suffixes = sorted([(text[i:], i) for i in range(n)])
    sa = [s[1] for s in suffixes]

    lcp = [0] * n
    if n > 0:
        inv_sa = [0] * n
        for i, rank in enumerate(sa):
            inv_sa[rank] = i
        k = 0
        for i in range(n):
            if inv_sa[i] == n - 1:
                k = 0
                continue
            j = sa[inv_sa[i] + 1]
            while i + k < n and j + k < n and text[i + k] == text[j + k]:
                k += 1
            lcp[inv_sa[i] + 1] = k
            if k > 0:
                k -= 1

    max_lcp = max(lcp) if lcp else 0
    repeated = ""
    if max_lcp > 0:
        idx = lcp.index(max_lcp)
        start_pos = sa[idx]
        repeated = text[start_pos:start_pos + max_lcp]

    return {"sa": sa, "lcp": lcp, "repeated": repeated}

def solve_aho(data):
    patterns = data.get("patterns", [])
    texts = data.get("texts", [])

    counts = []
    for text in texts:
        row = []
        for pat in patterns:
            cnt = 0
            if pat:
                start = 0
                while True:
                    idx = text.find(pat, start)
                    if idx == -1:
                        break
                    cnt += 1
                    start = idx + 1
            row.append(cnt)
        counts.append(row)

    return {"counts": counts}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            x = json.loads(line)
            t = x.get("task")

            if t == "ping":
                y = solve_ping(x)
            elif t == "lcs":
                y = solve_lcs(x)
            elif t == "merge":
                y = solve_merge(x)
            elif t == "tree":
                y = solve_tree(x)
            elif t in ("naive", "kmp", "rk"):
                y = solve_search(x, t)
            elif t == "suffix":
                y = solve_suffix(x)
            elif t == "aho":
                y = solve_aho(x)
            else:
                y = {"error": f"Unknown task {t}"}

            print(json.dumps(y))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()