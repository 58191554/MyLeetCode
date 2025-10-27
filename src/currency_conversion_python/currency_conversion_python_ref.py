import heapq
def convert(rates_str: str, src: str, dst: str, amt: float) -> float:
    rates = rates_str.split(",")
    graph = dict()
    for r in rates:
        r = r.strip()
        u, v, p = r.split(":")
        graph.setdefault(u, dict())
        graph[u][v] = eval(p)
    d = dict()
    pq = []
    heapq.heappush(pq, (-1, src))
    while pq:
        print(pq)
        p, x = heapq.heappop(pq)
        p = -p
        if x == dst:
            return p * amt
        if x in d:
            if d[x] <= p:
                continue
            else:
                return -1
        d[x] = p
        if x not in graph:
            continue
        for y in graph[x]:
            r = graph[x][y]
            if y not in d or d[y] < p * r:
                heapq.heappush(pq, (-p * r, y))
