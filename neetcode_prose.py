"""Original teaching prose for approaches whose licensed article omits a section.

A handful of upstream articles ship a working implementation and a complexity
analysis but no ``### Intuition`` or ``### Algorithm`` prose. ``build_neetcode``
falls back to this table so every approach tab explains itself. Keys are
``(problem number, approach title)`` and must match the parsed section heading
exactly; values fill only the fields the article leaves blank.

These explanations are authored for this project and follow the house format:
``intuition`` is a short paragraph naming the idea, ``algorithm`` is a numbered
walk of the committed code.
"""

PROSE = {
    (704, 'Built-In Function'): dict(
        intuition="Python's `bisect` module already implements binary search over a sorted "
        "sequence, so the only work left is turning an insertion point into an answer. "
        "`bisect_left` returns the first index where the target could be inserted while "
        "keeping the list sorted, which is exactly where the target sits if it is present "
        "at all.",
        algorithm="1. Call `bisect.bisect_left(nums, target)` to get the leftmost insertion point `index`.\n"
        "2. The insertion point can equal `len(nums)`, so check `index < len(nums)` before reading the array.\n"
        "3. Confirm `nums[index] == target`. The insertion point is defined even when the target is absent, so this comparison is what separates a hit from a miss.\n"
        "4. Return `index` when both checks pass, otherwise return `-1`.",
    ),
    (33, 'Binary Search (One Pass)'): dict(
        intuition="A rotated sorted array splits at the pivot into two sorted runs, and for any "
        "midpoint at least one side is guaranteed to be a clean sorted range. Compare the "
        "midpoint against the left endpoint to learn which half is sorted, then ask whether "
        "the target falls inside that half's value range. The test is reliable, so half the "
        "array can be discarded every step without ever locating the pivot.",
        algorithm="1. Set `l = 0` and `r = len(nums) - 1`, then loop while `l <= r`.\n"
        "2. Compute `mid` and return it immediately when `nums[mid] == target`.\n"
        "3. If `nums[l] <= nums[mid]` the left portion is sorted. The target lies outside it when `target > nums[mid]` or `target < nums[l]`, so move `l = mid + 1`; otherwise narrow to the left with `r = mid - 1`.\n"
        "4. Otherwise the right portion is sorted. The target lies outside it when `target < nums[mid]` or `target > nums[r]`, so move `r = mid - 1`; otherwise narrow to the right with `l = mid + 1`.\n"
        "5. Return `-1` once the window empties.",
    ),
    (226, 'Depth First Search'): dict(
        intuition="Inverting a tree means every node swaps its two children, and that single "
        "local action is the entire problem. Swap at the current node, then trust recursion "
        "to invert both subtrees; no extra bookkeeping is needed.",
        algorithm="1. Return `None` when `root` is empty. This is both the base case and the guard for missing children.\n"
        "2. Swap the children with `root.left, root.right = root.right, root.left`.\n"
        "3. Recurse into `root.left` and `root.right`. After the swap these name the original right and left subtrees, which is harmless because both are inverted either way.\n"
        "4. Return `root` so the caller receives the inverted tree.",
    ),
    (226, 'Breadth First Search'): dict(
        intuition="Each node's swap is independent of every other node, so the visiting order "
        "does not matter. A queue walks the tree level by level without recursion, which "
        "keeps a deep tree from bounding stack usage.",
        algorithm="1. Return `None` immediately for an empty root, then seed a `deque` with the root.\n"
        "2. While the queue is non-empty, take a node with `popleft()` and swap its two children.\n"
        "3. Enqueue whichever children now exist. The swap already happened, so `node.left` and `node.right` name the post-swap positions and each child is still enqueued exactly once.\n"
        "4. Return `root` when the queue drains.",
    ),
    (226, 'Iterative DFS'): dict(
        intuition="This is the breadth-first version with the queue replaced by a stack, which "
        "changes the visiting order to depth-first but not the result. Because every swap is "
        "independent, any traversal that reaches each node exactly once produces the same "
        "inverted tree.",
        algorithm="1. Return `None` for an empty root, then seed a list `stack` with the root.\n"
        "2. While the stack is non-empty, `pop()` a node and swap its children.\n"
        "3. Push the children that exist. `pop()` takes from the end, so one branch is followed to its bottom before the walk backtracks.\n"
        "4. Return `root`.",
    ),
    (104, 'Recursive DFS'): dict(
        intuition="The depth of a tree is one level for the current node plus the depth of its "
        "deeper subtree. Stated that way the problem defines itself: every node asks both "
        "children how deep they are and reports the larger answer plus one.",
        algorithm="1. Return `0` when `root` is `None`. An empty tree contributes no levels, which also covers missing children.\n"
        "2. Recursively compute `self.maxDepth(root.left)` and `self.maxDepth(root.right)`.\n"
        "3. Take `max` of the two results and add `1` for the current node.\n"
        "4. The value returned by the original call is the depth of the whole tree.",
    ),
    (104, 'Iterative DFS (Stack)'): dict(
        intuition="Recursion is a stack of pending nodes, so it can be carried explicitly. Pair "
        "every node with the depth it sits at, and the running maximum over all popped depths "
        "is the answer.",
        algorithm="1. Seed `stack` with `[root, 1]` and set `res = 0`.\n"
        "2. Pop a `[node, depth]` pair on each iteration.\n"
        "3. Skip falsy nodes. Children are pushed unconditionally, so `None` entries do reach the stack and are filtered here rather than before the push.\n"
        "4. For a real node, update `res = max(res, depth)` and push both children with `depth + 1`.\n"
        "5. Return `res` once the stack empties.",
    ),
    (104, 'Breadth First Search'): dict(
        intuition="Depth is a count of levels, and breadth-first search finishes exactly one "
        "level per outer iteration. Counting those iterations counts the levels directly, so "
        "no per-node depth has to be stored.",
        algorithm="1. Create a `deque` and enqueue `root` only when it exists, so an empty tree answers `0`.\n"
        "2. While the queue is non-empty, read `len(q)` as the size of the current level and pop exactly that many nodes.\n"
        "3. Enqueue each popped node's existing children. They belong to the next level and are not processed in this pass because the loop bound was fixed before it began.\n"
        "4. Increment `level` once per completed level and return it at the end.",
    ),
    (208, 'Prefix Tree (Hash Map)'): dict(
        intuition="A trie stores words by sharing their common prefixes: every edge is one "
        "character and every path from the root spells a prefix. Holding children in a hash "
        "map means a node pays only for the characters it actually has, and each operation "
        "becomes a walk of one step per character.",
        algorithm="1. `TrieNode` holds a `children` dictionary mapping a character to the next node, plus `endOfWord` marking that a complete word ends here.\n"
        "2. `insert` walks the word character by character, creating a missing child on demand, then sets `endOfWord = True` on the final node.\n"
        "3. `search` walks the same path but never creates nodes; a missing character means the word is absent. Arriving is not enough, so it returns `cur.endOfWord` and a stored word like `apple` does not make `app` report as present.\n"
        "4. `startsWith` is identical except that it returns `True` on arrival, since only the path has to exist.",
    ),
    (211, 'Depth First Search (Trie)'): dict(
        intuition="A plain trie walk breaks down once the pattern contains `.`, because that "
        "position could match any child. Turning the walk into a depth-first search fixes it: "
        "at a wildcard, branch into every child and accept if any branch succeeds. Ordinary "
        "characters stay a single deterministic step, so backtracking happens only where the "
        "pattern is genuinely ambiguous.",
        algorithm="1. `addWord` builds the trie exactly as an ordinary prefix tree, marking `word = True` on the final node.\n"
        "2. `search` calls `dfs(0, self.root)`, where `j` is the pattern index to resume from and `root` is the node reached so far.\n"
        "3. Inside `dfs`, walk forward from `j`. For a normal character, fail when it is missing from `cur.children`, otherwise descend.\n"
        "4. For `.`, try `dfs(i + 1, child)` against every child and return `True` if any succeeds, or `False` when all fail. The recursive call finishes the rest of the pattern, so the loop does not continue after branching.\n"
        "5. When the pattern is exhausted, return `cur.word` so a matched prefix is not mistaken for a stored word.",
    ),
    (78, 'Bit Manipulation'): dict(
        intuition="Each subset is a yes-or-no decision per element, so a subset is exactly an "
        "`n`-bit number: bit `j` set means `nums[j]` is included. Counting from `0` to "
        "`2^n - 1` therefore enumerates every subset once, with no recursion and no repeated "
        "work.",
        algorithm="1. Let `n = len(nums)` and loop `i` over `range(1 << n)`, the `2^n` possible masks.\n"
        "2. For each mask, build the subset by keeping every `nums[j]` whose bit is set, tested with `i & (1 << j)`.\n"
        "3. Append the subset to `res`.\n"
        "4. Return `res`. Distinct masks give distinct subsets, which relies on `nums` holding distinct values.",
    ),
    (778, "Kruskal's Algorithm"): dict(
        algorithm="1. Build a `DSU` over `N * N` cells, identifying cell `(r, c)` as `r * N + c`.\n"
        "2. Sort every cell into `positions` by elevation, so cells become usable in increasing time order.\n"
        "3. For each cell at time `t`, union it with any neighbour whose elevation is already at most `t`. Those are precisely the edges passable by time `t`.\n"
        "4. After each cell, test `dsu.connected(0, N * N - 1)`. The first time the two corners share a component, `t` is the earliest possible arrival, so return it.",
    ),
    (416, 'Dynamic Programming (Bitset)'): dict(
        intuition="The reachable-subset-sum table is a row of booleans, and a Python integer is "
        "already an arbitrarily wide array of bits. Keeping \"sum `s` is reachable\" in bit `s` "
        "lets a single shift-and-or update every sum at once, collapsing the inner loop of the "
        "usual dynamic program into one whole-word operation.",
        algorithm="1. Return `False` at once when `sum(nums)` is odd, since an odd total cannot split into two equal halves. Otherwise set `target = total // 2`.\n"
        "2. Start from `dp = 1 << 0`, meaning only the sum `0` is reachable before any element is used.\n"
        "3. For each `num`, apply `dp |= dp << num`. The shift moves every currently reachable sum up by `num`, and the or keeps the option of skipping that element.\n"
        "4. Test bit `target` with `(dp & (1 << target)) != 0`.",
    ),
}
