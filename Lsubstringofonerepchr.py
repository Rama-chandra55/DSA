class Solution(object):
    def longestRepeating(self, s, queryCharacters, queryIndices):
        n = len(s)
        tree_max = [0] * (4 * n)
        tree_pref = [0] * (4 * n)
        tree_suff = [0] * (4 * n)
        s = list(s)
        
        def pushup(node, l, r, mid):
            lc, rc = 2 * node, 2 * node + 1
            tree_pref[node] = tree_pref[lc]
            tree_suff[node] = tree_suff[rc]
            tree_max[node] = max(tree_max[lc], tree_max[rc])
            
            if s[mid] == s[mid + 1]:
                if tree_pref[lc] == mid - l + 1:
                    tree_pref[node] += tree_pref[rc]
                if tree_suff[rc] == r - mid:
                    tree_suff[node] += tree_suff[lc]
                tree_max[node] = max(tree_max[node], tree_suff[lc] + tree_pref[rc])
        
        def build(node, l, r):
            if l == r:
                tree_max[node] = tree_pref[node] = tree_suff[node] = 1
                return
            mid = (l + r) // 2
            build(2 * node, l, mid)
            build(2 * node + 1, mid + 1, r)
            pushup(node, l, r, mid)
            
        def update(node, l, r, idx, val):
            if l == r:
                s[idx] = val
                return
            mid = (l + r) // 2
            if idx <= mid:
                update(2 * node, l, mid, idx, val)
            else:
                update(2 * node + 1, mid + 1, r, idx, val)
            pushup(node, l, r, mid)

        build(1, 0, n - 1)
        ans = []
        for idx, char in zip(queryIndices, queryCharacters):
            update(1, 0, n - 1, idx, char)
            ans.append(tree_max[1])
            
        return ans
