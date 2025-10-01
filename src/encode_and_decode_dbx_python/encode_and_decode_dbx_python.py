class Solution:
    def encode(self, values):
        result = []
        cur = 0
        n = len(values)
        while (cur < n):
            is_rle = True
            x = values[cur]
            if cur + 7 >= n:
                for i in range(cur, n):
                    if x != values[i]:
                        is_rle = False
                        break
                if is_rle:
                    result.append("RLE[{},{}]".format(x, n - cur))
                    return result
            else:
                for i in range(8):
                    if values[cur + i] != x:
                        is_rle = False
                        break
            if is_rle:
                end = 8
                while cur + end < n and values[cur + end] == x:
                    end += 1
                result.append("RLE[{},{}]".format(x, end))
                cur += end
            else:
                result.append("BP[{}]".format(",".join(map(lambda x: str(x), values[cur: min(cur + 8, n)]))))
                cur += 8
        return result

    def decode(self, runs):
        result = []
        for p in runs:
            if p.split("[")[0] == "RLE":
                x, r = p[4:-1].split(",")
                result += [int(x)] * int(r)
            else:
                arr = list(map(lambda x: int(x), p[3:-1].split(",")))
                result += arr
        return result