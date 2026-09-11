"""Author and validate self-contained Python lessons; emit offline browser data."""
import json, textwrap, functools, pathlib

LESSONS=[]
def add(id,title,category,pattern,statement,intuition,meaning,state,base,body,order,result,params,setup,example,expected,time,space,opt,opt_note,notes,difficulty='Medium',rec_time='Exponential',rec_space='O(n)',extra=None):
    d=dict(id=id,title=title,category=category,pattern=pattern,statement=statement,intuition=intuition,meaning=meaning,state=state,base=base,body=body,order=order,result=result,params=params,setup=setup,example=example,expected=expected,time=time,space=space,opt=opt,opt_note=opt_note,notes=notes,difficulty=difficulty,rec_time=rec_time,rec_space=rec_space,extra=extra)
    LESSONS.append(d)
    return d

add(1,'Introduction to DP','1D DP','Overlapping subproblems','Given a non-negative integer n, return the nth Fibonacci number. F(0) = 0 and F(1) = 1. This lesson introduces the four ways to solve a DP recurrence.',
    ['To calculate F(5), you need F(4) and F(3). But F(4) also needs F(3). The same question appears in more than one branch: this is an overlapping subproblem.','Define the smallest complete question before choosing a table. Here only n determines the answer. Recursion expresses that question; memoization remembers its answer.','Bottom-up evaluation starts with the known answers 0 and 1. Every later number needs only the previous two, so a full table is optional.'],
    'f(i) is the ith Fibonacci number.',['i'],'if i < 2:\n    return i','return f(i - 1) + f(i - 2)',['for i in range(n + 1):'],'f(n)','n','',{'n':6},8,'O(n)','O(n)',
    'a, b = 0, 1\nfor _ in range(n):\n    a, b = b, a + b\nreturn a',
    'Only the previous two Fibonacci numbers remain live: O(n) time and O(1) auxiliary space. Python integers grow with n; these bounds count arithmetic operations.',
    ['DP needs a sufficient state, a recurrence, base cases, and a valid evaluation order.','Memoization removes repeated computation, not recursion depth. Python recursion is best kept to small teaching inputs.','Fast doubling can compute Fibonacci in O(log n) arithmetic operations; the linear method is the clearest introduction.'],'Easy','O(2^n)')

add(2,'Climbing Stairs','1D DP','Count ways','You are at step 0 of a staircase with n steps. Each move climbs 1 or 2 steps. Return the number of distinct ordered ways to reach step n. For n = 0, the empty sequence is one way.',
    ['Focus on the last move. To land on step i, you must have come from i − 1 with a one-step move or from i − 2 with a two-step move. These possibilities cannot overlap because their last moves differ.','Count the ways to reach each predecessor and add them. Do not choose the larger count: the task asks for all ways, not the best way.','Step 0 has one way, doing nothing. A negative step has zero ways. Those base cases make the same recurrence work for step 1 too.'],
    'f(i) counts ordered ways to reach step i.',['i'],'if i < 0:\n    return 0\nif i == 0:\n    return 1','return f(i - 1) + f(i - 2)',['for i in range(n + 1):'],'f(n)','n','',{'n':5},8,'O(n)','O(n)',
    'previous, current = 1, 1\nfor step in range(2, n + 1):\n    previous, current = current, previous + current\nreturn current',
    'Store only the counts for the last two steps. O(n) time, O(1) auxiliary space.',
    ['Recognize a count problem with a small set of legal last moves.','Order matters: [1, 2] and [2, 1] are different paths.','If allowed jump sizes change, sum over the allowed predecessors instead.'],'Easy','O(2^n)')

add(3,'Frog Jump','1D DP','Minimum cost to reach an index','A frog starts at index 0 of a nonempty heights array. It may jump forward by 1 or 2 indices. A jump from j to i costs abs(heights[i] − heights[j]). Return the minimum total energy to reach the last index.',
    ['Ask how the frog could have arrived at i. There are at most two predecessors. Each candidate combines the best cost already paid to reach that predecessor with the cost of the final jump.','The smaller immediate jump is not necessarily the best entire route. DP compares complete costs, including everything before that jump.','There is no cost to stand at index 0. Fill indices left to right so both candidate costs are already available.'],
    'f(i) is the minimum energy needed to reach index i.',['i'],'if i == 0:\n    return 0',
    'one = f(i - 1) + abs(heights[i] - heights[i - 1])\ntwo = float("inf")\nif i > 1:\n    two = f(i - 2) + abs(heights[i] - heights[i - 2])\nreturn min(one, two)',
    ['for i in range(n):'],'f(n - 1)','heights','n = len(heights)',{'heights':[10,20,30,10]},20,'O(n)','O(n)',
    'previous = before_previous = 0\nfor i in range(1, len(heights)):\n    one = previous + abs(heights[i] - heights[i - 1])\n    two = float("inf")\n    if i > 1:\n        two = before_previous + abs(heights[i] - heights[i - 2])\n    before_previous, previous = previous, min(one, two)\nreturn previous',
    'Only the two previous costs are needed. Preserve both before updating. O(n) time, O(1) space.',
    ['Recognize minimum cost plus a bounded number of previous positions.','Use infinity for an impossible choice in a minimization problem.','Use absolute height difference, not signed difference.'])

add(4,'Frog Jump with K Distance','1D DP','Bounded previous states','Given a nonempty heights array and k ≥ 1, a frog can jump from index j to any of the next k indices. Each jump costs the absolute height difference. Find the minimum energy to reach the last index.',
    ['The two choices in Frog Jump become up to k choices. For each i, try every legal jump length and add its edge cost to the predecessor answer.','Different paths still meet at the same index, so i is a sufficient state. The path used to get there does not affect future jump costs.','A circular buffer can retain only the last k costs. Read every predecessor before overwriting the slot for i.'],
    'f(i) is the minimum energy to reach i.',['i'],'if i == 0:\n    return 0','return min(f(i - jump) + abs(heights[i] - heights[i - jump])\n           for jump in range(1, min(k, i) + 1))',
    ['for i in range(n):'],'f(n - 1)','heights, k','n = len(heights)',{'heights':[10,30,40,20],'k':3},10,'O(nk)','O(n)',
    'width = min(k, len(heights))\nrecent = [0] * width\nfor i in range(1, len(heights)):\n    best = min(recent[(i - jump) % width]\n               + abs(heights[i] - heights[i - jump])\n               for jump in range(1, min(k, i) + 1))\n    recent[i % width] = best\nreturn recent[(len(heights) - 1) % width]',
    'Keep a ring of min(k, n) predecessor costs: O(nk) time and O(min(k, n)) space.',
    ['Bound jump lengths by i to avoid negative indexing in Python.','k = 1 leaves a single path. k ≥ n allows a direct jump.','The loop over choices multiplies the number of states in the time bound.'])

add(5,'Maximum Sum of Non-adjacent Elements','1D DP','Pick or skip','Given a list of non-negative numbers, choose a subset of indices with no two adjacent and return the maximum sum. Choosing no elements is allowed.',
    ['At index i, either skip the element and keep the optimum through i − 1, or pick it and combine it with the optimum through i − 2. Picking it forbids its neighbor.','These two cases cover every valid subset. Taking the maximum is correct because only the best sum matters.','The input prefix is enough to describe the subproblem; there is no need to remember an entire chosen subset.'],
    'f(i) is the maximum valid sum using indices 0 through i.',['i'],'if i < 0:\n    return 0','return max(f(i - 1), nums[i] + f(i - 2))',
    ['for i in range(n):'],'f(n - 1)','nums','n = len(nums)',{'nums':[2,1,4,9]},11,'O(n)','O(n)',
    'previous = before_previous = 0\nfor value in nums:\n    before_previous, previous = previous, max(previous, before_previous + value)\nreturn previous',
    'Keep the two prefix optima. O(n) time, O(1) space.',
    ['A pick-or-skip choice is common when items have local incompatibilities.','For all-negative inputs this version returns zero because the empty subset is allowed.','Update both rolling variables together to avoid mixing old and new states.'])

add(6,'House Robber II','1D DP','Break a cycle','Non-negative house values are arranged in a circle. Adjacent houses cannot both be robbed, including the first and last. Return the maximum amount. An empty street returns 0.',
    ['The ordinary non-adjacent recurrence forgets that the ends are neighbors. Break the circle into two valid lines: exclude the last house, or exclude the first.','Every valid selection excludes at least one of the two endpoints, so the better of those two cases is the global optimum. Overlap is harmless when taking a maximum.','Use the linear recurrence inside each range. A single house is a special case because excluding either endpoint would exclude that same house.'],
    'f(i, start) is the best sum from start through i within one linear case.',['i','start'],'if i < start:\n    return 0',
    'return max(f(i - 1, start), nums[i] + f(i - 2, start))',
    ['for start in (0, 1):','for i in range(start, n):'],'0 if n == 0 else nums[0] if n == 1 else max(f(n - 2, 0), f(n - 1, 1))','nums','n = len(nums)',{'nums':[2,3,2]},3,'O(n)','O(n)',
    'if len(nums) < 2:\n    return sum(nums)\ndef rob(start, end):\n    previous = before_previous = 0\n    for i in range(start, end):\n        before_previous, previous = previous, max(previous, before_previous + nums[i])\n    return previous\nreturn max(rob(0, len(nums) - 1), rob(1, len(nums)))',
    'Use index ranges rather than slices to keep the auxiliary space O(1). Time is O(n).',
    ['Do not solve a circular adjacency constraint as one linear array.','Handle n = 1 before splitting.','Excluding both endpoints is allowed and appears in both cases.'])

# Grids: states retain exactly the coordinates that determine future choices.
add(7,'Ninja’s Training','Grid DP','Last-choice constraint','For each day you have points for three activities. Choose exactly one activity per day, never repeating yesterday’s activity. Return the maximum total points. Empty input returns 0.',
    ['The day alone is not enough: the activity forbidden today depends on yesterday. Add that one piece of history to the state.','For a prefix ending on day d, try every activity except the forbidden one. The previous day must then avoid the activity chosen today.','There are four values of the forbidden marker: activities 0, 1, 2 and a sentinel 3 meaning no restriction. Only the previous day’s four scores are needed.'],
    'f(day, forbidden) is the best score through day, excluding forbidden on that day.',['day','forbidden'],'if day < 0:\n    return 0','return max(points[day][task] + f(day - 1, task)\n           for task in range(3) if task != forbidden)',
    ['for day in range(n):','for forbidden in range(4):'],'f(n - 1, 3)','points','n = len(points)',{'points':[[10,40,70],[20,50,80],[30,60,90]]},210,'O(n)','O(n)',
    'previous = [0] * 4\nfor day in points:\n    previous = [max(day[task] + previous[task]\n                    for task in range(3) if task != forbidden)\n                for forbidden in range(4)]\nreturn previous[3]',
    'Four scores per day suffice. O(n) time, O(1) auxiliary space. The list comprehension reads the old previous list before assignment.',
    ['A rule about the previous choice usually requires an extra state variable.','Use the no-restriction sentinel only for the final answer.','Exactly one activity is chosen even when all its points are negative.'])

add(8,'Unique Paths','Grid DP','Count grid paths','In an m × n grid with m, n ≥ 1, start at the top-left cell and move only right or down. Return the number of paths to the bottom-right cell.',
    ['The final move comes from above or from the left. Add the number of paths to those cells; their final moves distinguish the two groups.','The start contributes one empty path. Positions outside the grid contribute zero. The direction restriction makes the dependency graph acyclic.','Fill rows from top to bottom and columns left to right. The old entry in one rolling row represents above; the already updated previous entry represents left.'],
    'f(r, c) counts paths from (0, 0) to (r, c).',['r','c'],'if r < 0 or c < 0:\n    return 0\nif r == 0 and c == 0:\n    return 1','return f(r - 1, c) + f(r, c - 1)',
    ['for r in range(m):','for c in range(n):'],'f(m - 1, n - 1)','m, n','',{'m':3,'n':3},6,'O(mn)','O(mn)',
    'row = [0] * n\nrow[0] = 1\nfor _ in range(m):\n    for c in range(1, n):\n        row[c] += row[c - 1]\nreturn row[-1]',
    'Rolling row: O(mn) time, O(n) space. With no obstacles, math.comb(m + n - 2, m - 1) is a simpler combinatorial alternative: choose the positions of the down moves.',
    ['Count = sum of valid predecessor counts.','The initial 1 flows across the first row and down the first column.','The binomial shortcut applies only when every right/down route is allowed.'],'Easy',rec_space='O(m+n)')

add(9,'Unique Paths II','Grid DP','Obstacles in a grid','Given a nonempty rectangular grid containing 0 for a free cell and 1 for an obstacle, count right/down paths from the top-left to the bottom-right that avoid obstacles.',
    ['Keep the Unique Paths recurrence, but blocked cells must contribute zero. Check for an obstacle before declaring the start a valid path.','A barrier can cut off an entire region. In the rolling row, explicitly reset blocked cells to zero so stale counts cannot pass through them.','The number of rows and columns still determines the state count; obstacles change values, not the dimensions of the state.'],
    'f(r, c) counts valid paths to cell (r, c).',['r','c'],'if r < 0 or c < 0 or grid[r][c] == 1:\n    return 0\nif r == 0 and c == 0:\n    return 1','return f(r - 1, c) + f(r, c - 1)',
    ['for r in range(m):','for c in range(n):'],'f(m - 1, n - 1)','grid','m, n = len(grid), len(grid[0])',{'grid':[[0,0,0],[0,1,0],[0,0,0]]},2,'O(mn)','O(mn)',
    'row = [0] * len(grid[0])\nrow[0] = 1\nfor cells in grid:\n    for c, blocked in enumerate(cells):\n        if blocked:\n            row[c] = 0\n        elif c:\n            row[c] += row[c - 1]\nreturn row[-1]',
    'Reset obstacles in a rolling row. O(mn) time, O(n) space.',
    ['Check the obstacle before the start base case.','A blocked destination or start makes the answer zero.','This lesson uses 1 as blocked; some judge versions use −1. Adapt that comparison.'],rec_space='O(m+n)')

add(10,'Minimum Path Sum','Grid DP','Minimum weighted path','Given a nonempty rectangular integer grid, return the minimum sum of cell values on a path from top-left to bottom-right using only right and down moves. Include both endpoint values.',
    ['Every route into a cell pays its value once. Choose the cheaper of the best routes from above and left, then add the current value.','Out-of-bounds is impossible and should cost infinity. Zero would create an artificial free route from outside the grid.','Negative cell values are safe because movement never creates a cycle. The same left-to-right row order works.'],
    'f(r, c) is the minimum cost of a path ending at (r, c).',['r','c'],'if r < 0 or c < 0:\n    return float("inf")\nif r == 0 and c == 0:\n    return grid[0][0]','return grid[r][c] + min(f(r - 1, c), f(r, c - 1))',
    ['for r in range(m):','for c in range(n):'],'f(m - 1, n - 1)','grid','m, n = len(grid), len(grid[0])',{'grid':[[1,3,1],[1,5,1],[4,2,1]]},7,'O(mn)','O(mn)',
    'row = [float("inf")] * len(grid[0])\nrow[0] = 0\nfor cells in grid:\n    for c, cost in enumerate(cells):\n        left = row[c - 1] if c else float("inf")\n        row[c] = cost + min(row[c], left)\nreturn row[-1]',
    'One row contains above and left at the right times. O(mn) time, O(n) space.',
    ['Minimum total cost is different from minimum local edge cost.','Use +infinity for unreachable minimum-cost states.','Do not add the start cell twice.'],rec_space='O(m+n)')

add(11,'Triangle Minimum Path Sum','Grid DP','Variable-width rows','Given a nonempty triangle, row r has r + 1 numbers. Starting at the top, move to column c or c + 1 in the next row. Return the minimum path sum to any cell in the bottom row.',
    ['Define the answer looking downward: from (r, c), the next cell is directly below or diagonally below-right.','Any bottom-row cell is a valid endpoint and returns its own value. This avoids a separate minimum over endpoints.','Tabulate upward from the last row. In a rolling array, scanning left to right preserves both children until they have been read.'],
    'f(r, c) is the minimum cost from (r, c) to the bottom.',['r','c'],'if r == n - 1:\n    return triangle[r][c]','return triangle[r][c] + min(f(r + 1, c), f(r + 1, c + 1))',
    ['for r in range(n - 1, -1, -1):','for c in range(r + 1):'],'f(0, 0)','triangle','n = len(triangle)',{'triangle':[[2],[3,4],[6,5,7],[4,1,8,3]]},11,'O(n²)','O(n²)',
    'row = triangle[-1][:]\nfor r in range(len(triangle) - 2, -1, -1):\n    for c in range(r + 1):\n        row[c] = triangle[r][c] + min(row[c], row[c + 1])\nreturn row[0]',
    'Copy the bottom row and fold upward without changing the input. O(n²) time, O(n) space.',
    ['The direction of the recurrence decides the direction of tabulation.','Unlike a rectangle, only columns 0 through r exist in row r.','Updating right to left would overwrite a needed child.'])

add(12,'Minimum Falling Path Sum','Grid DP','Multiple starting points','For a nonempty rectangular integer matrix, start anywhere in the top row. On each next row move straight down, down-left, or down-right. Return the minimum sum to the bottom row.',
    ['A cell in the current row has up to three predecessors. Add its value to the cheapest predecessor answer.','Every top-row cell can start a path. Treat each of those values as a base case, then take the minimum of the last row.','The maximum-sum variant is the same structure with max and negative infinity. Be consistent about which objective you solve.'],
    'f(r, c) is the minimum sum of a falling path ending at (r, c).',['r','c'],'if c < 0 or c >= n:\n    return float("inf")\nif r == 0:\n    return matrix[0][c]','return matrix[r][c] + min(f(r - 1, c - 1), f(r - 1, c), f(r - 1, c + 1))',
    ['for r in range(m):','for c in range(n):'],'min(f(m - 1, c) for c in range(n))','matrix','m, n = len(matrix), len(matrix[0])',{'matrix':[[2,1,3],[6,5,4],[7,8,9]]},13,'O(mn)','O(mn)',
    'previous = matrix[0][:]\nfor cells in matrix[1:]:\n    current = []\n    for c, value in enumerate(cells):\n        best = min(previous[max(0, c - 1):min(len(cells), c + 2)])\n        current.append(value + best)\n    previous = current\nreturn min(previous)',
    'Use two rows: O(mn) time and O(n + m) auxiliary space in this Python version because matrix[1:] copies m row references. Replace that slice with a row-index loop for O(n) space.',
    ['There is no fixed starting column.','Guard both column boundaries before indexing.','For maximum falling sum, swap min for max and +infinity for −infinity.'],rec_space='O(m)')

add(13,'Cherry Pickup II','Grid DP','Two agents, shared row','Two robots start at (0, 0) and (0, n − 1) of a nonempty m × n non-negative grid. Both move down one row, with column change −1, 0, or +1. Collect visited cell values, counting a shared cell once. Return the maximum total.',
    ['Both robots have advanced the same number of rows, so a single row coordinate is enough. Keep both column coordinates because future choices depend on each.','Each robot has three moves, creating nine pairs to compare. Add both current cells unless their columns coincide.','The state space is m × n × n. Fold rows upward using two n × n layers; merging the robot columns would lose valid joint choices.'],
    'f(r, a, b) is the maximum collection from row r onward with robots in columns a and b.',['r','a','b'],'if a < 0 or a >= n or b < 0 or b >= n:\n    return -float("inf")\nif r == m:\n    return 0',
    'gain = grid[r][a] + (grid[r][b] if a != b else 0)\nreturn gain + max(f(r + 1, a + da, b + db)\n                  for da in (-1, 0, 1) for db in (-1, 0, 1))',
    ['for r in range(m - 1, -1, -1):','for a in range(n):','for b in range(n):'],'f(0, 0, n - 1)','grid','m, n = len(grid), len(grid[0])',{'grid':[[3,1,1],[2,5,1],[1,5,5]]},21,'O(mn²)','O(mn²)',
    'n = len(grid[0])\nnext_row = [[0] * n for _ in range(n)]\nfor r in range(len(grid) - 1, -1, -1):\n    current = [[0] * n for _ in range(n)]\n    for a in range(n):\n        for b in range(n):\n            future = max(next_row[x][y]\n                         for x in range(max(0, a - 1), min(n, a + 2))\n                         for y in range(max(0, b - 1), min(n, b + 2)))\n            current[a][b] = grid[r][a] + (grid[r][b] if a != b else 0) + future\n    next_row = current\nreturn next_row[0][n - 1]',
    'Retain only the next joint-position layer: O(mn²) time, O(n²) space.',
    ['Synchronized agents share the time coordinate, but each needs its own position.','If a == b, count the cell only once.','Out-of-grid robot positions are invalid, not zero-value choices.'],'Hard',rec_space='O(m)')

# Subsequences and capacities. Non-negative values are required for sum-indexed DP.
subset_body='return f(i - 1, target) or (nums[i] <= target and f(i - 1, target - nums[i]))'
count_body='ways = f(i - 1, target)\nif nums[i] <= target:\n    ways += f(i - 1, target - nums[i])\nreturn ways'
subset_base='if i < 0:\n    return target == 0'
count_base='if i < 0:\n    return int(target == 0)'
subset_opt='dp = [False] * (target + 1)\ndp[0] = True\nfor value in nums:\n    for total in range(target, value - 1, -1):\n        dp[total] = dp[total] or dp[total - value]\nreturn dp[target]'
count_opt='dp = [0] * (target + 1)\ndp[0] = 1\nfor value in nums:\n    for total in range(target, value - 1, -1):\n        dp[total] += dp[total - value]\nreturn dp[target]'
add(14,'Subset Sum Equal to Target','Subsequences','0/1 pick or skip','Given non-negative integers nums and target ≥ 0, determine whether a subset sums to target. Each index may be used at most once; the empty subset sums to zero.',
    ['At the last available index, either ignore it or spend its value from the remaining target. Both branches move to i − 1 because an item can be used only once.','Index alone is insufficient: the answer also depends on how much sum remains. That makes a two-dimensional state.','When compressing the table, traverse target sums downward. This keeps the pick branch tied to the previous item layer.'],
    'f(i, target) says whether indices 0 through i can form target.',['i','target'],subset_base,subset_body,
    ['for i in range(n):','for target in range(goal + 1):'],'f(n - 1, goal)','nums, target','n, goal = len(nums), target',{'nums':[1,2,3,4],'target':4},True,'O(nT)','O(nT)',subset_opt,
    'A descending sum loop uses O(T) space and O(nT) time, where T is the target. This is pseudo-polynomial in the numeric target.',
    ['An item plus a remaining capacity suggests a pick/skip state.','Descending sums prevent reusing the current item.','A bitset is a compact alternative: bits |= bits << value, then inspect the target bit. Mask if the total can grow huge.'])

add(15,'Partition Equal Subset Sum','Subsequences','Reduce to subset sum','Given non-negative integers nums, decide whether every element can be assigned to one of two subsets with equal sums. Empty subsets are allowed.',
    ['If the total is S, both subsets must sum to S/2. An odd total can never be split equally.','For an even total, finding one subset with sum S/2 is enough: the complement automatically has the same sum.','This reduction reuses the 0/1 subset state without adding a second subset dimension. Every index is either in the chosen subset or its complement.'],
    'f(i, target) tests whether the first i + 1 values can form target.',['i','target'],subset_base,subset_body,
    ['for i in range(n):','for target in range(goal + 1):'],'total % 2 == 0 and f(n - 1, goal)','nums','n, total = len(nums), sum(nums)\ngoal = total // 2',{'nums':[1,5,11,5]},True,'O(nS)','O(nS)',
    'total = sum(nums)\nif total % 2:\n    return False\ntarget = total // 2\n'+subset_opt,
    'Reduce the capacity to S/2 and use a descending boolean row. O(nS) time, O(S) space, S = total sum.',
    ['Equal partition is a decision problem, not an optimization over both subsets.','Always check parity.','The numeric total controls memory; this is unsuitable for huge values without another technique.'])

add(16,'Minimum Subset Sum Difference','Subsequences','Reachable sums','Partition all non-negative integers in nums into two subsets and minimize the absolute difference of their sums. Empty subsets are allowed.',
    ['For a chosen sum s and total S, the complement has sum S − s. Their difference is abs(S − 2s).','Compute which sums are reachable, then inspect the reachable sum closest to S/2. You do not need to store two subset sums.','The recurrence is boolean feasibility, even though the final problem is an optimization. The minimum is taken after the reachability table is built.'],
    'f(i, target) says whether a subset of indices up to i reaches target.',['i','target'],subset_base,subset_body,
    ['for i in range(n):','for target in range(goal + 1):'],'min(total - 2 * s for s in range(goal + 1) if f(n - 1, s))','nums','n, total = len(nums), sum(nums)\ngoal = total // 2',{'nums':[1,6,11,5]},1,'O(nS)','O(nS)',
    'total = sum(nums)\ntarget = total // 2\ndp = [False] * (target + 1)\ndp[0] = True\nfor value in nums:\n    for s in range(target, value - 1, -1):\n        dp[s] = dp[s] or dp[s - value]\nreturn min(total - 2 * s for s in range(target + 1) if dp[s])',
    'One row of reachable sums up to half the total: O(nS) time, O(S) space.',
    ['Express the objective using one subset sum and the total.','Only sums at or below half are needed by symmetry.','The closest numeric sum is useful only if it is reachable.'])

add(17,'Count Subsets with Sum K','Subsequences','Count 0/1 subsets','Given non-negative nums and target ≥ 0, count index subsets whose values sum to target. Equal values at different indices are distinct choices. Return the exact count.',
    ['Replace the feasibility OR with addition: the subsets skipping the current index and the subsets taking it are disjoint.','Do not return immediately when target becomes zero: remaining zero values can each be picked or skipped, doubling the count.','The clean base case runs out of indices: one way if the remaining target is zero, otherwise zero. This handles zeros naturally.'],
    'f(i, target) counts subsets from indices 0 through i summing to target.',['i','target'],count_base,count_body,
    ['for i in range(n):','for target in range(goal + 1):'],'f(n - 1, goal)','nums, target','n, goal = len(nums), target',{'nums':[0,1,2,3],'target':3},4,'O(nT)','O(nT)',count_opt,
    'Descending sums retain 0/1 semantics in O(T) space and O(nT) time. A zero value doubles every count once.',
    ['Counting uses + where feasibility uses OR.','Zeros matter even after the target reaches zero.','This version returns exact Python integers. Apply a modulus if the judge requests one.'])

add(18,'Count Partitions with Given Difference','Subsequences','Algebraic reduction','Assign every index in non-negative nums to labeled subsets S1 and S2 such that sum(S1) − sum(S2) = difference ≥ 0. Count the assignments exactly.',
    ['Write the two equations: S1 + S2 = total and S1 − S2 = difference. Therefore S2 = (total − difference)/2.','If the numerator is negative or odd, no assignment exists. Otherwise count subsets with the reduced target.','The subsets are labeled. For difference zero, exchanging S1 and S2 is a different assignment unless the index assignments coincide.'],
    'f(i, target) counts choices for the second subset from the first i + 1 indices.',['i','target'],count_base,count_body,
    ['for i in range(n):','for target in range(goal + 1):'],'0 if delta < 0 or delta % 2 else f(n - 1, goal)','nums, difference','n = len(nums)\ndelta = sum(nums) - difference\ngoal = max(0, delta // 2)',{'nums':[5,2,6,4],'difference':3},1,'O(nS)','O(nS)',
    'delta = sum(nums) - difference\nif delta < 0 or delta % 2:\n    return 0\ntarget = delta // 2\n'+count_opt,
    'Count a single target using O(S) space and O(nS) time. S denotes the input sum.',
    ['Two partition equations can eliminate one dimension.','Check non-negativity and parity before allocating the table.','Preserve the subset-counting zero behavior.'])

add(19,'0/1 Knapsack','Subsequences','Value under capacity','Given equally sized weights and values arrays with positive weights, choose each item at most once to maximize total value without exceeding a non-negative capacity. Choosing nothing is allowed.',
    ['Skipping an item preserves capacity. Taking it earns its value and reduces capacity by its weight. Both cases discard that item from future consideration.','The state needs an item boundary and remaining capacity. Weight and value play different roles; only weight indexes the capacity axis.','For one-row tabulation, iterate capacity downward. Updating upward would allow this same item to contribute repeatedly.'],
    'f(i, cap) is the maximum value using items 0 through i within cap.',['i','cap'],'if i < 0:\n    return 0',
    'best = f(i - 1, cap)\nif weights[i] <= cap:\n    best = max(best, values[i] + f(i - 1, cap - weights[i]))\nreturn best',
    ['for i in range(n):','for cap in range(capacity + 1):'],'f(n - 1, capacity)','weights, values, capacity','n = len(weights)',{'weights':[1,2,4,5],'values':[5,4,8,6],'capacity':5},13,'O(nW)','O(nW)',
    'dp = [0] * (capacity + 1)\nfor weight, value in zip(weights, values):\n    for cap in range(capacity, weight - 1, -1):\n        dp[cap] = max(dp[cap], value + dp[cap - weight])\nreturn dp[capacity]',
    'Descending capacities keep each item single-use: O(nW) time and O(W) space.',
    ['At most capacity differs from exactly filling capacity. Zero initialization is valid here.','Do not choose by value/weight ratio: fractional-knapsack greediness fails for indivisible items.','W is the capacity, so the time bound is pseudo-polynomial.'])

add(20,'Minimum Coins','Subsequences','Unbounded minimum','Given distinct positive coin denominations and amount ≥ 0, find the fewest coins needed to make the amount using unlimited copies. Return −1 if impossible.',
    ['Choose the final coin. Removing its value leaves a smaller amount with the same denominations available. This removes the need for an item dimension when minimizing coin count.','An amount of zero needs zero coins; an unreachable positive amount has infinite cost. Each valid final coin adds one.','This amounts-only recurrence is a cleaner alternative to the two-dimensional unbounded-knapsack formulation. It has the same O(nA) time bound.'],
    'f(remaining) is the minimum number of coins needed for remaining.',['remaining'],'if remaining == 0:\n    return 0',
    'return min((1 + f(remaining - coin) for coin in coins if coin <= remaining),\n           default=float("inf"))',
    ['for remaining in range(amount + 1):'],'-1 if f(amount) == float("inf") else f(amount)','coins, amount','',{'coins':[1,2,5],'amount':11},3,'O(nA)','O(A)',
    'dp = [0] + [float("inf")] * amount\nfor remaining in range(1, amount + 1):\n    dp[remaining] = min((1 + dp[remaining - coin]\n                         for coin in coins if coin <= remaining),\n                        default=float("inf"))\nreturn -1 if dp[amount] == float("inf") else dp[amount]',
    'The amount-only formulation already uses O(A) space and O(nA) time. A two-scalar rolling window is not generally valid because arbitrary denominations refer far backward.',
    ['Positive denominations guarantee that recursion makes progress.','A greedy largest-coin strategy fails for coins [1, 3, 4] and amount 6.','Use infinity internally and convert to −1 only at the API boundary.'],rec_space='O(A)')

add(21,'Target Sum','Subsequences','Signs become subsets','Place either + or − before every non-negative integer in nums. Count assignments whose signed total equals target, which may be negative.',
    ['Group plus-signed values into P and minus-signed values into N. P − N = target and P + N = total, so N = (total − target)/2.','Reject |target| > total and odd differences. Then count index subsets with sum N, keeping zeros as distinct sign choices.','Each zero has two signs even though both contribute zero. Correct subset counting automatically captures this doubling.'],
    'f(i, target) counts the index subsets chosen to receive a minus sign.',['i','target'],count_base,count_body,
    ['for i in range(n):','for target in range(goal + 1):'],'0 if abs(wanted) > total or delta % 2 else f(n - 1, goal)','nums, target','n, total, wanted = len(nums), sum(nums), target\ndelta = total - wanted\ngoal = max(0, delta // 2)',{'nums':[1,1,1,1,1],'target':3},5,'O(nS)','O(nS)',
    'total = sum(nums)\nif abs(target) > total or (total - target) % 2:\n    return 0\ntarget = (total - target) // 2\n'+count_opt,
    'Reduce to a one-row subset count: O(nS) time and O(S) space for valid targets. A dictionary of signed sums is useful when the dense sum range is too large.',
    ['Signs turn into a partition equation.','A zero creates two assignments, +0 and −0.','Do not treat duplicate values as identical indices.'])

add(22,'Coin Change II','Subsequences','Unbounded combinations','Given distinct positive coin denominations and amount ≥ 0, count combinations summing to amount with unlimited copies. Coin order does not distinguish combinations.',
    ['Keep an item dimension to enforce a canonical denomination order. Skip a denomination by moving to i − 1; take it by staying at i and reducing the amount.','Staying at the same index is what makes the supply unlimited. Positive coin values ensure the remaining amount decreases.','In the one-row version, process coins outside and amounts in ascending order. Reversing those loop roles counts ordered sequences instead.'],
    'f(i, remaining) counts combinations using denominations 0 through i.',['i','remaining'],'if i < 0:\n    return int(remaining == 0)',
    'ways = f(i - 1, remaining)\nif coins[i] <= remaining:\n    ways += f(i, remaining - coins[i])\nreturn ways',
    ['for i in range(n):','for remaining in range(amount + 1):'],'f(n - 1, amount)','coins, amount','n = len(coins)',{'coins':[1,2,5],'amount':5},4,'O(nA)','O(nA)',
    'dp = [0] * (amount + 1)\ndp[0] = 1\nfor coin in coins:\n    for remaining in range(coin, amount + 1):\n        dp[remaining] += dp[remaining - coin]\nreturn dp[amount]',
    'Coin-first, ascending amounts: O(nA) time and O(A) space.',
    ['Combination counting needs a fixed denomination order.','Ascending sums allow reuse; descending sums mean 0/1 usage.','Duplicate denominations should be removed before calling this version.'],rec_space='O(n+A)')

add(23,'Unbounded Knapsack','Subsequences','Unlimited pick or skip','Given positive weights, corresponding values, and capacity ≥ 0, maximize total value with unlimited copies of each item. The capacity need not be completely filled.',
    ['Unlike 0/1 knapsack, picking an item does not remove it from consideration. Stay at i and subtract its weight from capacity.','The skip branch still moves to the previous item, ensuring all possibilities are covered. A positive weight makes the take branch smaller.','In a compressed table, ascending capacity intentionally reuses an answer updated for the current item.'],
    'f(i, cap) is the best value using unlimited copies of items 0 through i.',['i','cap'],'if i < 0:\n    return 0',
    'best = f(i - 1, cap)\nif weights[i] <= cap:\n    best = max(best, values[i] + f(i, cap - weights[i]))\nreturn best',
    ['for i in range(n):','for cap in range(capacity + 1):'],'f(n - 1, capacity)','weights, values, capacity','n = len(weights)',{'weights':[2,4,6],'values':[5,11,13],'capacity':10},27,'O(nW)','O(nW)',
    'dp = [0] * (capacity + 1)\nfor weight, value in zip(weights, values):\n    for cap in range(weight, capacity + 1):\n        dp[cap] = max(dp[cap], value + dp[cap - weight])\nreturn dp[capacity]',
    'Ascending capacities use O(W) space and O(nW) time.',
    ['Take stays at i; skip goes to i − 1.','A zero-weight positive-value item would make the optimum unbounded, so weights must be positive.','Initialization with zero allows unused capacity and skipping negative-value items.'],rec_space='O(n+W)')

add(24,'Rod Cutting','Subsequences','Exact-fill unbounded knapsack','prices[i − 1] is the selling price of a piece of length i. A rod has length len(prices). Cut it into positive integer lengths to maximize total revenue; the whole rod must be used.',
    ['Choose the first piece length, earn its price, then optimally cut the remaining rod. Every length remains available.','Length zero has zero revenue. Every positive length is fillable because a length-one price exists.','This is exact-fill unbounded knapsack with weights 1 through n. The amount-only recurrence is especially clear.'],
    'f(length) is the maximum revenue from exactly length units of rod.',['length'],'if length == 0:\n    return 0',
    'return max(prices[piece - 1] + f(length - piece)\n           for piece in range(1, length + 1))',
    ['for length in range(n + 1):'],'f(n)','prices','n = len(prices)',{'prices':[2,5,7,8,10]},12,'O(n²)','O(n)',
    'dp = [0] * (len(prices) + 1)\nfor length in range(1, len(prices) + 1):\n    dp[length] = max(prices[piece - 1] + dp[length - piece]\n                     for piece in range(1, length + 1))\nreturn dp[-1]',
    'The amount-only table already uses O(n) space and O(n²) time. All earlier lengths can be dependencies, so two scalars are not enough.',
    ['Piece lengths are implicit: index + 1.','Exactly filling the rod is required even if prices are negative.','Do not add a cost for cutting unless the problem explicitly defines one.'])

lcs_base='if i == 0 or j == 0:\n    return 0'
lcs_body='if a[i - 1] == b[j - 1]:\n    return 1 + f(i - 1, j - 1)\nreturn max(f(i - 1, j), f(i, j - 1))'
lcs_opt='previous = [0] * (len(b) + 1)\nfor x in a:\n    current = [0] * (len(b) + 1)\n    for j, y in enumerate(b, 1):\n        current[j] = 1 + previous[j - 1] if x == y else max(previous[j], current[j - 1])\n    previous = current\nreturn previous[-1]'
add(25,'Longest Common Subsequence','Strings','Two-prefix alignment','Given strings a and b, return the length of their longest common subsequence. Characters may be deleted, but the order of retained characters must remain unchanged.',
    ['Compare the last characters of two prefixes. If they match, extend an optimum from both shorter prefixes by one.','If they differ, they cannot both be the last matched character. Discard one endpoint and try both possibilities, taking the larger answer.','Use prefix lengths rather than last indices: an empty prefix has length zero, and actual characters are at i − 1 and j − 1.'],
    'f(i, j) is the LCS length of a[:i] and b[:j].',['i','j'],lcs_base,lcs_body,
    ['for i in range(m + 1):','for j in range(n + 1):'],'f(m, n)','a, b','m, n = len(a), len(b)',{'a':'abcde','b':'ace'},3,'O(mn)','O(mn)',lcs_opt,
    'Two rows use O(n) space and O(mn) time. Swap a and b first if you want the shorter string to determine the row width.',
    ['Two sequences and order-preserving matching suggest two prefix lengths.','Subsequence does not require contiguity.','Keeping only rows gives the length; ordinary reconstruction needs the full table or a divide-and-conquer method.'],rec_space='O(m+n)')

print_lcs_body='if a[i - 1] == b[j - 1]:\n    return f(i - 1, j - 1) + a[i - 1]\nleft, up = f(i - 1, j), f(i, j - 1)\nreturn left if len(left) >= len(up) else up'
print_lcs_opt='m, n = len(a), len(b)\ndp = [[0] * (n + 1) for _ in range(m + 1)]\nfor i in range(1, m + 1):\n    for j in range(1, n + 1):\n        dp[i][j] = 1 + dp[i - 1][j - 1] if a[i - 1] == b[j - 1] else max(dp[i - 1][j], dp[i][j - 1])\ni, j = m, n\nanswer = []\nwhile i and j:\n    if a[i - 1] == b[j - 1]:\n        answer.append(a[i - 1])\n        i, j = i - 1, j - 1\n    elif dp[i - 1][j] >= dp[i][j - 1]:\n        i -= 1\n    else:\n        j -= 1\nreturn "".join(reversed(answer))'
add(26,'Print Longest Common Subsequence','Strings','Reconstruct an optimum','Given two strings, return one actual longest common subsequence. If several are valid, any is accepted. This implementation breaks ties by moving up in the length table.',
    ['A length tells you how good a solution is, but not which characters it contains. The teaching recurrence stores the chosen string to make reconstruction explicit.','For a match, append the shared character. For a mismatch, retain the longer candidate string. This is clear but string copying costs extra.','The efficient version stores lengths, then walks backward. A matched diagonal contributes a character; otherwise move to a neighbor with the same optimum. Reverse the collected characters.'],
    'f(i, j) returns one LCS string for the two prefixes.',['i','j'],'if i == 0 or j == 0:\n    return ""',print_lcs_body,
    ['for i in range(m + 1):','for j in range(n + 1):'],'f(m, n)','a, b','m, n = len(a), len(b)',{'a':'abcde','b':'ace'},'ace','O(mnL)','O(mnL)',print_lcs_opt,
    'Store lengths instead of strings: O(mn + L) time, O(mn + L) space including reconstruction. L is the LCS length. Hirschberg’s algorithm can reduce working memory to linear space but is more involved.',
    ['Follow decisions that preserve the optimum.','Multiple correct strings may exist; a tie policy makes output deterministic.','Repeated string concatenation is why the teaching variants cost O(mnL).'],rec_space='O((m+n)L)')

add(27,'Longest Common Substring','Strings','Contiguous matching suffix','Given strings a and b, return the length of their longest common contiguous substring.',
    ['A substring must be contiguous. Define the state as the matching suffix ending at the two prefix boundaries.','Matching characters extend the diagonal suffix by one. A mismatch resets the suffix to zero; taking max of neighbors inside the state would accidentally allow gaps.','The longest substring can end anywhere, so take the maximum over all suffix states rather than only the bottom-right cell.'],
    'f(i, j) is the common suffix length of a[:i] and b[:j].',['i','j'],lcs_base,'return 1 + f(i - 1, j - 1) if a[i - 1] == b[j - 1] else 0',
    ['for i in range(m + 1):','for j in range(n + 1):'],'max((f(i, j) for i in range(m + 1) for j in range(n + 1)), default=0)','a, b','m, n = len(a), len(b)',{'a':'abcjklp','b':'acjkp'},3,'O(mn)','O(mn)',
    'row = [0] * (len(b) + 1)\nbest = 0\nfor x in a:\n    for j in range(len(b), 0, -1):\n        row[j] = 1 + row[j - 1] if x == b[j - 1] else 0\n        best = max(best, row[j])\nreturn best',
    'Scan columns right to left to preserve the old diagonal. O(mn) time, O(n) space.',
    ['Contiguous matching means reset on mismatch.','The answer is the maximum cell, not necessarily f(m, n).','Suffix trees/automata offer faster asymptotic methods, with substantially more machinery.'],rec_time='O(mn min(m,n))',rec_space='O(min(m,n))')

add(28,'Longest Palindromic Subsequence','Strings','Match interval endpoints','Given a string s, return the maximum length of a subsequence that reads the same forward and backward.',
    ['If the two endpoints match, they can surround an optimum palindrome from the inside. Add two and shrink both boundaries.','If they differ, a palindrome cannot use both as its outer pair. Try removing each endpoint, keeping the longer answer.','An empty interval has length zero and a single character has length one. Alternatively, the length equals LCS(s, reverse(s)).'],
    'f(i, j) is the longest palindromic subsequence length inside s[i:j+1].',['i','j'],'if i > j:\n    return 0\nif i == j:\n    return 1',
    'if s[i] == s[j]:\n    return 2 + f(i + 1, j - 1)\nreturn max(f(i + 1, j), f(i, j - 1))',
    ['for i in range(n - 1, -1, -1):','for j in range(i, n):'],'f(0, n - 1)','s','n = len(s)',{'s':'bbbab'},4,'O(n²)','O(n²)',
    'n = len(s)\ndp = [0] * n\nfor i in range(n - 1, -1, -1):\n    diagonal = 0\n    dp[i] = 1\n    for j in range(i + 1, n):\n        old = dp[j]\n        dp[j] = diagonal + 2 if s[i] == s[j] else max(dp[j], dp[j - 1])\n        diagonal = old\nreturn dp[-1] if n else 0',
    'One row plus the saved old diagonal: O(n²) time and O(n) space.',
    ['A palindrome suggests pairing two interval endpoints.','Subsequence allows deleting interior characters.','For LCS with the reverse, the length is safe; naive reconstruction can require extra care to produce a palindrome.'])

add(29,'Minimum Insertions to Make a Palindrome','Strings','Preserve a palindromic core','Insert characters anywhere into s to make it a palindrome. Return the minimum number of insertions; existing characters cannot be removed or reordered.',
    ['Matching endpoints already mirror one another, so recurse into the interior for free.','When endpoints differ, insert a copy of one endpoint on the opposite side. Pay one, then choose which boundary to resolve.','Equivalently, preserve a longest palindromic subsequence and mirror every other character. The answer is n minus its length.'],
    'f(i, j) is the fewest insertions needed for s[i:j+1].',['i','j'],'if i >= j:\n    return 0',
    'if s[i] == s[j]:\n    return f(i + 1, j - 1)\nreturn 1 + min(f(i + 1, j), f(i, j - 1))',
    ['for i in range(n - 1, -1, -1):','for j in range(i, n):'],'f(0, n - 1)','s','n = len(s)',{'s':'mbadm'},2,'O(n²)','O(n²)',
    'n = len(s)\ndp = [0] * n\nfor i in range(n - 1, -1, -1):\n    diagonal = 0\n    for j in range(i + 1, n):\n        old = dp[j]\n        dp[j] = diagonal if s[i] == s[j] else 1 + min(dp[j], dp[j - 1])\n        diagonal = old\nreturn dp[-1] if n else 0',
    'Save the old diagonal while rolling intervals into one row. O(n²) time, O(n) space.',
    ['Resolve unequal endpoints by mirroring one of them.','A string already palindromic needs zero insertions.','The identity n − LPS is useful for recognizing the pattern quickly.'])

add(30,'Minimum Insertions and Deletions to Convert a String','Strings','Keep the LCS','Convert string a to string b using only single-character insertions and deletions. Return the fewest operations. Replacement is not a single allowed operation.',
    ['Keep an LCS unchanged. Delete the characters of a outside it, then insert the missing characters of b.','If the LCS has length L, the total is (m − L) + (n − L). Any conversion preserves a common subsequence, so preserving the longest is optimal.','Do not confuse this with edit distance, where replacing one character costs one instead of a delete plus an insert.'],
    'f(i, j) is the LCS length retained between the two prefixes.',['i','j'],lcs_base,lcs_body,
    ['for i in range(m + 1):','for j in range(n + 1):'],'m + n - 2 * f(m, n)','a, b','m, n = len(a), len(b)',{'a':'heap','b':'pea'},3,'O(mn)','O(mn)',lcs_opt.replace('return previous[-1]','return len(a) + len(b) - 2 * previous[-1]'),
    'Use rolling LCS lengths. O(mn) time and O(n) space.',
    ['When insert/delete preserves order, look for a common subsequence to keep.','A replacement here costs two operations.','The answer is m + n − 2L, not max(m, n) − L.'],rec_space='O(m+n)')

scs_body='if a[i - 1] == b[j - 1]:\n    return f(i - 1, j - 1) + a[i - 1]\nx = f(i - 1, j) + a[i - 1]\ny = f(i, j - 1) + b[j - 1]\nreturn x if len(x) <= len(y) else y'
scs_opt='m, n = len(a), len(b)\ndp = [[0] * (n + 1) for _ in range(m + 1)]\nfor i in range(m + 1):\n    dp[i][0] = i\nfor j in range(n + 1):\n    dp[0][j] = j\nfor i in range(1, m + 1):\n    for j in range(1, n + 1):\n        dp[i][j] = 1 + (dp[i - 1][j - 1] if a[i - 1] == b[j - 1] else min(dp[i - 1][j], dp[i][j - 1]))\ni, j, answer = m, n, []\nwhile i and j:\n    if a[i - 1] == b[j - 1]:\n        answer.append(a[i - 1])\n        i, j = i - 1, j - 1\n    elif dp[i - 1][j] <= dp[i][j - 1]:\n        answer.append(a[i - 1])\n        i -= 1\n    else:\n        answer.append(b[j - 1])\n        j -= 1\nreturn a[:i] + b[:j] + "".join(reversed(answer))'
add(31,'Shortest Common Supersequence','Strings','Merge around shared characters','Return one shortest string that contains both a and b as subsequences. Multiple answers may be valid.',
    ['If both endpoints match, write that character once and solve both shorter prefixes.','If they differ, write one endpoint after a supersequence that already contains the other prefix. Compare both lengths.','The teaching recurrence returns strings directly. To avoid repeated copying, the efficient version stores lengths and reconstructs backward, adding leftover prefix characters at the end.'],
    'f(i, j) returns one shortest supersequence of a[:i] and b[:j].',['i','j'],'if i == 0:\n    return b[:j]\nif j == 0:\n    return a[:i]',scs_body,
    ['for i in range(m + 1):','for j in range(n + 1):'],'f(m, n)','a, b','m, n = len(a), len(b)',{'a':'abac','b':'cab'},'cabac','O(mn(m+n))','O(mn(m+n))',scs_opt,
    'Store integer lengths and backtrack: O(mn + m + n) time and O(mn + m + n) space. Full-table reconstruction is clearer than advanced linear-space divide and conquer.',
    ['Shared matched characters appear once in the supersequence.','The optimal length is m + n − LCS(a, b).','Append the unmatched remaining prefix when one index reaches zero.'],'Hard',rec_space='O((m+n)²)')

add(32,'Distinct Subsequences','Strings','Count ways to match a target','Given source string a and target string b, count the index subsequences of a that equal b. Different index choices count separately. Return an exact integer.',
    ['If the current characters match, either use this source character to match the target endpoint or skip it. Add the two disjoint counts.','If they differ, only skipping the source character is legal. The target still needs the same endpoint.','The empty target occurs once in any source, including the empty source. A nonempty target cannot occur in an empty source.'],
    'f(i, j) counts ways to form b[:j] as a subsequence of a[:i].',['i','j'],'if j == 0:\n    return 1\nif i == 0:\n    return 0',
    'ways = f(i - 1, j)\nif a[i - 1] == b[j - 1]:\n    ways += f(i - 1, j - 1)\nreturn ways',
    ['for i in range(m + 1):','for j in range(n + 1):'],'f(m, n)','a, b','m, n = len(a), len(b)',{'a':'babgbag','b':'bag'},5,'O(mn)','O(mn)',
    'dp = [1] + [0] * len(b)\nfor x in a:\n    for j in range(len(b), 0, -1):\n        if x == b[j - 1]:\n            dp[j] += dp[j - 1]\nreturn dp[-1]',
    'Descending target positions keep each source character single-use. O(mn) time, O(n) space.',
    ['Use +, not max: you are counting distinct index selections.','Handle the empty target before the empty source.','An ascending target loop would reuse the same source character.'],'Hard',rec_space='O(m+n)')

add(33,'Edit Distance','Strings','Three edit choices','Convert a to b using insert, delete, or replace of one character, each costing 1. Return the minimum number of edits.',
    ['Matching endpoints cost nothing and reduce both prefixes. For different endpoints, consider each allowed operation.','Delete consumes a source character only; insert resolves a target character only; replace resolves both. Add one to the minimum of those predecessor costs.','An empty prefix needs as many insertions or deletions as the length of the other prefix. These form the first row and column.'],
    'f(i, j) is the minimum edit cost from a[:i] to b[:j].',['i','j'],'if i == 0:\n    return j\nif j == 0:\n    return i',
    'if a[i - 1] == b[j - 1]:\n    return f(i - 1, j - 1)\nreturn 1 + min(f(i - 1, j), f(i, j - 1), f(i - 1, j - 1))',
    ['for i in range(m + 1):','for j in range(n + 1):'],'f(m, n)','a, b','m, n = len(a), len(b)',{'a':'horse','b':'ros'},3,'O(mn)','O(mn)',
    'previous = list(range(len(b) + 1))\nfor i, x in enumerate(a, 1):\n    current = [i] + [0] * len(b)\n    for j, y in enumerate(b, 1):\n        current[j] = previous[j - 1] if x == y else 1 + min(previous[j], current[j - 1], previous[j - 1])\n    previous = current\nreturn previous[-1]',
    'Two rows suffice when only the distance is needed. O(mn) time, O(n) space.',
    ['Draw insert, delete, and replace as three moves through the prefix table.','Match costs zero; replacement costs one only when different.','Weighted edit variants use different transition costs but the same state.'],'Hard',rec_space='O(m+n)')

add(34,'Wildcard Matching','Strings','Match with flexible tokens','Decide whether the entire text matches pattern. ? matches exactly one character; * matches any sequence, including empty. Other characters match literally.',
    ['A literal or ? consumes one character from each side. A star can disappear, or consume one text character while remaining available.','For *, OR the state without the star and the state with one fewer text character. Those options cover zero or more matched characters.','An empty text matches a prefix only when every pattern character there is *. Precompute that boundary to avoid repeatedly scanning prefixes.'],
    'f(i, j) says whether pattern[:i] matches all of text[:j].',['i','j'],'if i == 0:\n    return j == 0\nif j == 0:\n    return stars[i]',
    'if pattern[i - 1] == "*":\n    return f(i - 1, j) or f(i, j - 1)\nif pattern[i - 1] == "?" or pattern[i - 1] == text[j - 1]:\n    return f(i - 1, j - 1)\nreturn False',
    ['for i in range(m + 1):','for j in range(n + 1):'],'f(m, n)','pattern, text','m, n = len(pattern), len(text)\nstars = [True]\nfor char in pattern:\n    stars.append(stars[-1] and char == "*")',{'pattern':'*a?b','text':'aab'},True,'O(mn+m)','O(mn+m)',
    'previous = [True] + [False] * len(text)\nfor token in pattern:\n    current = [previous[0] and token == "*"] + [False] * len(text)\n    for j, char in enumerate(text, 1):\n        if token == "*":\n            current[j] = previous[j] or current[j - 1]\n        elif token == "?" or token == char:\n            current[j] = previous[j - 1]\n    previous = current\nreturn previous[-1]',
    'Rolling prefixes use O(n) space and O(mn + m) time. Greedy backtracking to the last star can use O(1) space, though naive implementations have quadratic worst cases.',
    ['The star has an empty branch and a consume branch.','Question mark consumes exactly one character, never zero.','Wildcard syntax here is not regular-expression syntax.'],'Hard',rec_space='O(m+n)')

# Stock variants share the same holding state, with explicit transaction semantics.
stock_base='if day == n:\n    return 0 if holding == 0 else -float("inf")'
stock_body='skip = f(day + 1, holding)\nif holding:\n    return max(skip, prices[day] + f(day + 1, 0))\nreturn max(skip, -prices[day] + f(day + 1, 1))'
limited_base='if day == n or left == 0:\n    return 0 if holding == 0 else -float("inf")'
limited_body='skip = f(day + 1, holding, left)\nif holding:\n    return max(skip, prices[day] + f(day + 1, 0, left - 1))\nreturn max(skip, -prices[day] + f(day + 1, 1, left))'
add(35,'Best Time to Buy and Sell Stock I','Stocks','One transaction','Given non-negative daily prices, buy one share and sell it on a later day at most once. Return the maximum profit; doing nothing is allowed.',
    ['A transaction has two actions: buy and sell. The teaching state records whether a share is held and whether a sale remains.','When flat, buying subtracts today’s price. When holding, selling adds today’s price and consumes the sale allowance. You may always skip a day.','For one transaction, an even simpler solution keeps the cheapest earlier price and the best profit from selling today. No table is needed.'],
    'f(day, holding, left) is future profit with 0/1 share held and left sales allowed.',['day','holding','left'],limited_base,limited_body,
    ['for day in range(n - 1, -1, -1):','for holding in range(2):','for left in range(limit + 1):'],'f(0, 0, limit)','prices','n, limit = len(prices), 1',{'prices':[7,1,5,3,6,4]},5,'O(n)','O(n)',
    'cheapest = float("inf")\nbest = 0\nfor price in prices:\n    best = max(best, price - cheapest)\n    cheapest = min(cheapest, price)\nreturn best',
    'A running minimum gives O(n) time and O(1) space. This is simpler than the general stock DP for one transaction.',
    ['Keep the minimum price from earlier days.','You cannot sell before buying.','A descending price series has profit zero.'],'Easy')

add(36,'Best Time to Buy and Sell Stock II','Stocks','Unlimited transactions','Given non-negative daily prices, maximize profit with any number of completed buy/sell transactions. Hold at most one share at a time. Each action occurs on its own day.',
    ['The future decision depends on the day and whether you own a share. When flat you may buy; when holding you may sell.','No counter is needed because transactions are unlimited. The recurrence compares action against skipping.','With no fees or cooldown, each positive consecutive price increase can be collected. Splitting a rising run into daily gains gives the same profit as buying its low and selling its high.'],
    'f(day, holding) is the maximum future profit from that day and inventory state.',['day','holding'],stock_base,stock_body,
    ['for day in range(n - 1, -1, -1):','for holding in range(2):'],'f(0, 0)','prices','n = len(prices)',{'prices':[7,1,5,3,6,4]},7,'O(n)','O(n)',
    'return sum(max(0, prices[i] - prices[i - 1])\n           for i in range(1, len(prices)))',
    'Sum positive adjacent differences: O(n) time, O(1) auxiliary space. Greedy is valid specifically because there is no fee, limit, or cooldown.',
    ['Holding is the minimum history needed to know which action is legal.','Do not use this positive-differences shortcut when there are extra trading constraints.','Ending while holding is invalid in this recurrence, represented by −infinity.'])

limited_opt='limit = min(k, len(prices) // 2)\nif limit == 0:\n    return 0\nif k >= len(prices) // 2:\n    return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))\nfuture = [[0] * (limit + 1), [-float("inf")] * (limit + 1)]\nfor price in reversed(prices):\n    current = [[0] * (limit + 1), [-float("inf")] * (limit + 1)]\n    for left in range(1, limit + 1):\n        current[0][left] = max(future[0][left], -price + future[1][left])\n        current[1][left] = max(future[1][left], price + future[0][left - 1])\n    future = current\nreturn future[0][limit]'
for id,title,k in [(37,'Best Time to Buy and Sell Stock III',2),(38,'Best Time to Buy and Sell Stock IV',None)]:
    add(id,title,'Stocks','Limited transactions',
        'Given non-negative daily prices, maximize profit with at most '+('two' if k else 'k ≥ 0')+' completed transactions. Hold at most one share; buy before selling.',
        ['Add a transaction allowance to the day and holding state. We count a transaction when its sell completes, so buying does not decrement the allowance.','Selling adds the current price and reduces remaining sales by one. Skipping preserves inventory and the allowance.','No schedule can complete more than floor(n/2) buy/sell pairs on separate days. If k is that large, the limit is irrelevant and the unlimited shortcut applies.'],
        'f(day, holding, left) is the best future profit with left sales remaining.',['day','holding','left'],limited_base,limited_body,
        ['for day in range(n - 1, -1, -1):','for holding in range(2):','for left in range(limit + 1):'],'f(0, 0, limit)',
        'prices' if k else 'prices, k','n, limit = len(prices), 2' if k else 'n, limit = len(prices), min(k, len(prices) // 2)',
        {'prices':[3,3,5,0,0,3,1,4]} if k else {'prices':[2,4,1,7],'k':2},6 if k else 8,
        'O(n)' if k else 'O(n min(k,n))','O(n)' if k else 'O(n min(k,n))',
        ('k = 2\n' if k else '')+limited_opt,
        'Two time layers: '+('O(n) time and O(1) space for a fixed limit of two.' if k else 'O(n min(k,n)) time, O(min(k,n)) space; O(n) time when the unlimited shortcut applies.'),
        ['Choose a convention: decrement the allowance on selling, consistently.','At zero transactions, a holding state cannot complete its position.','State count is days × inventory states × transaction allowances.'],'Hard')

add(39,'Stock with Cooldown','Stocks','A delayed next decision','Maximize profit with unlimited buy/sell transactions, holding at most one share. After selling on day d, you cannot buy on day d + 1. Prices are non-negative.',
    ['The only change from unlimited trading is the state after selling: skip the next day and resume flat at day + 2.','A buy still advances one day into a holding state. A skip advances one day without changing inventory.','Because a sale reads two days ahead, space compression needs two future layers, not only tomorrow.'],
    'f(day, holding) is the best future profit when the next legal action is on day.',['day','holding'],'if day >= n:\n    return 0 if holding == 0 else -float("inf")',
    'skip = f(day + 1, holding)\nif holding:\n    return max(skip, prices[day] + f(day + 2, 0))\nreturn max(skip, -prices[day] + f(day + 1, 1))',
    ['for day in range(n - 1, -1, -1):','for holding in range(2):'],'f(0, 0)','prices','n = len(prices)',{'prices':[1,2,3,0,2]},3,'O(n)','O(n)',
    'tomorrow = [0, -float("inf")]\nafter_tomorrow = [0, -float("inf")]\nfor price in reversed(prices):\n    current = [max(tomorrow[0], -price + tomorrow[1]),\n               max(tomorrow[1], price + after_tomorrow[0])]\n    after_tomorrow, tomorrow = tomorrow, current\nreturn tomorrow[0]',
    'Retain two future days: O(n) time and O(1) space.',
    ['A forced waiting period changes the transition’s time jump.','The cooldown follows selling, not buying.','Positive daily differences overcount profit because immediate re-entry is forbidden.'])

add(40,'Stock with Transaction Fee','Stocks','Charge at one boundary','Given non-negative daily prices and a non-negative fee, maximize profit with unlimited transactions and at most one held share. Pay the fee once per completed transaction.',
    ['Keep the unlimited-trading state. Subtract the fee on the sell branch, so each completed transaction is charged exactly once.','Small local rises may not cover the fee. DP naturally decides whether to hold through them instead of selling and rebuying.','You may charge on buying instead, but never on both boundaries. Two values for the next day are sufficient.'],
    'f(day, holding) is maximum future profit with a fee charged on each sale.',['day','holding'],stock_base,
    'skip = f(day + 1, holding)\nif holding:\n    return max(skip, prices[day] - fee + f(day + 1, 0))\nreturn max(skip, -prices[day] + f(day + 1, 1))',
    ['for day in range(n - 1, -1, -1):','for holding in range(2):'],'f(0, 0)','prices, fee','n = len(prices)',{'prices':[1,3,2,8,4,9],'fee':2},8,'O(n)','O(n)',
    'flat, holding = 0, -float("inf")\nfor price in reversed(prices):\n    flat, holding = max(flat, -price + holding), max(holding, price - fee + flat)\nreturn flat',
    'Two future-state values give O(n) time and O(1) space. Simultaneous assignment uses the previous values on both right-hand sides.',
    ['Charge the fee exactly once per transaction.','The optimal strategy can hold through small dips to avoid another fee.','At fee = 0, this reduces to Stock II.'])

lis_body='return 1 + max((f(j) for j in range(i) if nums[j] < nums[i]), default=0)'
lis_fast='from bisect import bisect_left\ntails = []\nfor value in nums:\n    position = bisect_left(tails, value)\n    if position == len(tails):\n        tails.append(value)\n    else:\n        tails[position] = value\nreturn len(tails)'
add(41,'Longest Increasing Subsequence','LIS','Best chain ending here','Given an integer list nums, return the length of its longest strictly increasing subsequence. Preserve index order; elements need not be adjacent.',
    ['Instead of storing a previous chosen index, ask for the best increasing subsequence that ends exactly at i. Its predecessor must be earlier and strictly smaller.','Start with the one-element subsequence, then extend each valid predecessor. The global optimum may end anywhere.','For length alone, maintain the smallest possible tail for each subsequence length. Replacing a tail with a smaller value keeps future extensions easier.'],
    'f(i) is the LIS length ending exactly at index i.',['i'],'if i < 0:\n    return 0',lis_body,
    ['for i in range(n):'],'max((f(i) for i in range(n)), default=0)','nums','n = len(nums)',{'nums':[10,9,2,5,3,7,101,18]},4,'O(n²)','O(n)',lis_fast,
    'Patience sorting with bisect_left: O(n log n) time, O(n) space. This improves time rather than the worst-case space of the endpoint DP.',
    ['An optimum chain ending at a position avoids a two-index state.','Strictly increasing means <, not ≤.','The tails array gives the length, but its values need not themselves form an input subsequence.'])

print_lis_opt='from bisect import bisect_left\ntails, tail_indices = [], []\nparent = [-1] * len(nums)\nfor i, value in enumerate(nums):\n    pos = bisect_left(tails, value)\n    if pos:\n        parent[i] = tail_indices[pos - 1]\n    if pos == len(tails):\n        tails.append(value)\n        tail_indices.append(i)\n    else:\n        tails[pos] = value\n        tail_indices[pos] = i\nanswer = []\ni = tail_indices[-1] if tail_indices else -1\nwhile i != -1:\n    answer.append(nums[i])\n    i = parent[i]\nreturn tuple(reversed(answer))'
add(42,'Print Longest Increasing Subsequence','LIS','Remember predecessors','Return one longest strictly increasing subsequence of nums as a tuple. Multiple answers may be correct.',
    ['A predecessor link explains where each optimal endpoint answer came from. The teaching recurrence stores tuples directly to make that chain visible.','For each valid previous endpoint, extend its tuple by the current value and keep the longest. This makes copying expensive.','The improved version combines binary-search tails with actual input indices and parent links. Follow the final endpoint’s parents, then reverse the result.'],
    'f(i) returns one longest increasing subsequence ending at i.',['i'],'if i < 0:\n    return ()',
    'previous = max((f(j) for j in range(i) if nums[j] < nums[i]), key=len, default=())\nreturn previous + (nums[i],)',
    ['for i in range(n):'],'max((f(i) for i in range(n)), key=len, default=())','nums','n = len(nums)',{'nums':[3,1,2,4,6]},(1,2,4,6),'O(n²)','O(n²)',print_lis_opt,
    'Parent links plus binary-search tails use O(n log n) time and O(n) space. Different tie choices may return different valid LIS tuples.',
    ['Store indices, not just tail values, when reconstructing.','A replaced tail does not erase the parent history of earlier endpoints.','The displayed example may have several optimal answers; compare validity and length.'])

add(43,'LIS with Binary Search','LIS','Smallest tail per length','Return the length of the longest strictly increasing subsequence. This workshop focuses on improving the O(n²) endpoint DP to O(n log n).',
    ['For each possible length, remember the smallest tail of any increasing subsequence seen so far. A smaller tail can accept every future extension that a larger tail can.','Find the first tail greater than or equal to the current value with bisect_left. Replace it, or append if no such tail exists.','The tails remain sorted, enabling binary search. Equal values replace a tail instead of increasing the length, preserving strictness.'],
    'The baseline f(i) is the LIS ending at i; the faster invariant is tails[length − 1].',['i'],'if i < 0:\n    return 0',lis_body,
    ['for i in range(n):'],'max((f(i) for i in range(n)), default=0)','nums','n = len(nums)',{'nums':[2,5,3,7,11,8,10]},5,'O(n²)','O(n)',lis_fast,
    'Binary-search replacement is O(log n) per element, giving O(n log n) time and O(n) space.',
    ['tails[k] is a minimum endpoint, not the kth value of a fixed subsequence.','bisect_left solves strict LIS; bisect_right solves longest non-decreasing subsequence.','A replacement improves future potential without increasing the current best length.'])

add(44,'Largest Divisible Subset','LIS','Sort to expose a chain','Given distinct positive integers, return a largest tuple in which for every pair one value divides the other. The output is sorted in ascending order.',
    ['Sort the values. If a smaller value divides a larger one, it is a legal predecessor in a chain.','Divisibility is transitive: if a divides b and b divides c, then a divides c. Therefore a chain of adjacent divisibility relationships guarantees the pairwise condition.','Use LIS-style length and parent arrays. Sorting is allowed because this asks for a subset, not an order-preserving input subsequence.'],
    'f(i) returns a largest divisible chain ending at sorted value nums[i].',['i'],'if i < 0:\n    return ()',
    'previous = max((f(j) for j in range(i) if nums[i] % nums[j] == 0), key=len, default=())\nreturn previous + (nums[i],)',
    ['for i in range(n):'],'max((f(i) for i in range(n)), key=len, default=())','nums','nums = sorted(nums)\nn = len(nums)',{'nums':[1,2,4,8]},(1,2,4,8),'O(n²)','O(n²)',
    'nums = sorted(nums)\nif not nums:\n    return ()\nlength = [1] * len(nums)\nparent = [-1] * len(nums)\nfor i in range(len(nums)):\n    for j in range(i):\n        if nums[i] % nums[j] == 0 and length[j] + 1 > length[i]:\n            length[i], parent[i] = length[j] + 1, j\ni = max(range(len(nums)), key=lambda i: length[i])\nanswer = []\nwhile i != -1:\n    answer.append(nums[i])\n    i = parent[i]\nreturn tuple(reversed(answer))',
    'Lengths and parent pointers replace copied tuples: O(n²) time, O(n) space including the sorted copy.',
    ['Sort when the problem is about a subset and order is unrestricted.','Zero is excluded because divisibility checks would divide by zero.','Binary-search LIS tails do not directly apply to the divisibility relation.'])

chain_setup='words = sorted(words, key=len)\nn = len(words)\ndef predecessor(a, b):\n    if len(b) != len(a) + 1:\n        return False\n    i = 0\n    for char in b:\n        if i < len(a) and a[i] == char:\n            i += 1\n    return i == len(a)'
add(45,'Longest String Chain','LIS','A custom predecessor relation','Given a list of words, find the longest chain where each next word can be made by inserting exactly one character into the previous word without reordering its characters.',
    ['Sort words by length so possible predecessors appear earlier. Equal-length words can never be adjacent in a valid chain.','The baseline compares earlier words and checks whether inserting one character creates the current word. Then use the best chain ending there.','A faster way generates every predecessor by deleting one character of the current word and looks up its chain length in a dictionary.'],
    'f(i) is the longest chain ending at words[i] after sorting by length.',['i'],'if i < 0:\n    return 0',
    'return 1 + max((f(j) for j in range(i) if predecessor(words[j], words[i])), default=0)',
    ['for i in range(n):'],'max((f(i) for i in range(n)), default=0)','words',chain_setup,{'words':['a','b','ba','bca','bda','bdca']},4,'O(n²L)','O(n)',
    'best = {}\nfor word in sorted(words, key=len):\n    length = 1\n    for i in range(len(word)):\n        previous = word[:i] + word[i + 1:]\n        length = max(length, 1 + best.get(previous, 0))\n    best[word] = max(best.get(word, 0), length)\nreturn max(best.values(), default=0)',
    'Generate L deletions, each costing O(L) in Python: O(nL² + n log n) time, O(n + L) auxiliary references/temporary characters beyond the input strings.',
    ['This is LIS with a word-predecessor relationship.','The longer word must have exactly one extra character.','Account for Python slicing and hashing costs in the faster method.'])

add(46,'Longest Bitonic Subsequence','LIS','Join two directional chains','Return the maximum length of a subsequence that strictly increases and then strictly decreases. This version allows either side to have length one, so a monotone subsequence also qualifies.',
    ['Choose a peak. The best bitonic subsequence through it combines the LIS ending there with the decreasing subsequence starting there.','Compute increasing lengths from left to right and decreasing lengths from right to left. Add the two and subtract one because the peak appears in both.','If a judge requires both sides to have an actual change, restrict candidate peaks to increasing[i] > 1 and decreasing[i] > 1.'],
    'f(direction, i) is the increasing length ending at i (0), or decreasing length starting at i (1).',['direction','i'],'if i < 0 or i >= n:\n    return 0',
    'indices = range(i) if direction == 0 else range(i + 1, n)\nreturn 1 + max((f(direction, j) for j in indices if nums[j] < nums[i]), default=0)',
    ['for direction in range(2):','for i in (range(n) if direction == 0 else range(n - 1, -1, -1)):'],'max((f(0, i) + f(1, i) - 1 for i in range(n)), default=0)','nums','n = len(nums)',{'nums':[1,11,2,10,4,5,2,1]},6,'O(n²)','O(n)',
    'from bisect import bisect_left\ndef lengths(values):\n    tails, result = [], []\n    for value in values:\n        pos = bisect_left(tails, value)\n        if pos == len(tails):\n            tails.append(value)\n        else:\n            tails[pos] = value\n        result.append(pos + 1)\n    return result\nleft = lengths(nums)\nright = lengths(reversed(nums))[::-1]\nreturn max((a + b - 1 for a, b in zip(left, right)), default=0)',
    'Binary-search lengths from both directions yield O(n log n) time and O(n) space.',
    ['A shared pivot often lets two directional DPs meet.','Subtract the peak once.','Check whether the problem permits a purely increasing or decreasing answer.'])

add(47,'Number of Longest Increasing Subsequences','LIS','Track length and count','Return the number of index-distinct longest strictly increasing subsequences in nums. Empty input returns 0.',
    ['At each endpoint, keep both the best length and how many ways attain it. A scalar count alone cannot tell whether a candidate is optimal.','A longer candidate replaces both values. An equally long candidate adds its count. A shorter candidate contributes nothing.','After processing endpoints, add counts only for endpoints whose lengths equal the overall maximum. Equal values do not extend each other.'],
    'f(i) returns (best length ending at i, number of ways to obtain it).',['i'],'if i < 0:\n    return (0, 0)',
    'length, count = 1, 1\nfor j in range(i):\n    if nums[j] < nums[i]:\n        previous_length, ways = f(j)\n        if previous_length + 1 > length:\n            length, count = previous_length + 1, ways\n        elif previous_length + 1 == length:\n            count += ways\nreturn (length, count)',
    ['for i in range(n):'],'sum(f(i)[1] for i in range(n) if f(i)[0] == max((f(j)[0] for j in range(n)), default=0))','nums','n = len(nums)',{'nums':[1,3,5,4,7]},2,'O(n²)','O(n)',
    'n = len(nums)\nlength, count = [1] * n, [1] * n\nfor i in range(n):\n    for j in range(i):\n        if nums[j] < nums[i]:\n            if length[j] + 1 > length[i]:\n                length[i], count[i] = length[j] + 1, count[j]\n            elif length[j] + 1 == length[i]:\n                count[i] += count[j]\nbest = max(length, default=0)\nreturn sum(count[i] for i in range(n) if length[i] == best)',
    'Endpoint arrays already use O(n) space, with O(n²) time. A coordinate-compressed Fenwick tree storing (length, count) pairs improves time to O(n log n), but simple tails cannot count alternatives.',
    ['Replace counts for a better length; add counts only for a tie.','All equal values produce n subsequences of length one.','Count index choices, not distinct value sequences.'])

mcm_body='return min(f(i, k) + f(k + 1, j) + dims[i - 1] * dims[k] * dims[j]\n           for k in range(i, j))'
mcm_opt='n = len(dims) - 1\ndp = [[0] * (n + 1) for _ in range(n + 1)]\nfor length in range(2, n + 1):\n    for i in range(1, n - length + 2):\n        j = i + length - 1\n        dp[i][j] = min(dp[i][k] + dp[k + 1][j] + dims[i - 1] * dims[k] * dims[j]\n                       for k in range(i, j))\nreturn dp[1][n] if n else 0'
for id,title in [(48,'Matrix Chain Multiplication'),(49,'Matrix Chain: Tabulation Workshop')]:
    add(id,title,'Partition DP','Try the final split','Matrix i has shape dims[i − 1] × dims[i], where dims has at least two positive integers. Choose parenthesization of the product to minimize scalar multiplications. Matrix order cannot change.',
        ['Choose the final multiplication. Splitting between k and k + 1 leaves two independent chains, whose optimal products have known outer dimensions.','The merge cost is dims[i − 1] × dims[k] × dims[j]. Add it to the optimal left and right costs, then minimize over k.','Fill intervals in increasing length, or decreasing left endpoint with increasing right endpoint. Both orders place every smaller interval before its parent.'],
        'f(i, j) is the minimum cost to multiply matrices i through j, inclusive.',['i','j'],'if i >= j:\n    return 0',mcm_body,
        ['for i in range(n, 0, -1):','for j in range(i, n + 1):'],'f(1, n)','dims','n = len(dims) - 1',{'dims':[10,20,30,40]},18000,'O(n³)','O(n²)',mcm_opt,
        'The dense interval table uses O(n²) space and O(n³) time. A rolling row is not valid: split points can reference many earlier intervals. This tabulation workshop shows the clear length-first ordering.',
        ['Independent left and right subproblems suggest interval partition DP.','A single matrix costs zero multiplications.','Do not confuse the split matrix index k with the shared dimension dims[k].'],'Hard',rec_time='O(3^n)')

add(50,'Minimum Cost to Cut a Stick','Partition DP','Choose the first cut','Given stick length > 0 and distinct cut positions strictly inside it, perform every cut. Each cut costs the length of the current piece. Return the minimum total cost.',
    ['Choose the first cut within an interval. It costs the full current piece length, then separates the remaining cuts into independent left and right pieces.','Sort cut positions and add endpoints 0 and length. If remaining cuts are i through j, the piece boundaries are cuts[i − 1] and cuts[j + 1].','An interval with no cuts costs zero. Try every first cut; its physical position determines both subproblems.'],
    'f(i, j) is the minimum cost to perform sorted cuts i through j.',['i','j'],'if i > j:\n    return 0',
    'return cuts[j + 1] - cuts[i - 1] + min(f(i, k - 1) + f(k + 1, j)\n                                       for k in range(i, j + 1))',
    ['for i in range(n, 0, -1):','for j in range(i, n + 1):'],'f(1, n)','length, cuts','cuts = [0] + sorted(cuts) + [length]\nn = len(cuts) - 2',{'length':7,'cuts':[1,3,4,5]},16,'O(c³ + c log c)','O(c²)',
    'positions = [0] + sorted(cuts) + [length]\nsize = len(positions)\ndp = [[0] * size for _ in range(size)]\nfor gap in range(2, size):\n    for left in range(size - gap):\n        right = left + gap\n        dp[left][right] = positions[right] - positions[left] + min(\n            dp[left][k] + dp[k][right] for k in range(left + 1, right))\nreturn dp[0][-1]',
    'Keep the O(c²) interval table; ordinary rolling rows lose required intervals. Time is O(c³ + c log c), c = number of cuts. Knuth optimization applies to this interval-cost structure and can reduce DP time to O(c²).',
    ['The first cut creates independent subproblems.','The cost is the current segment length, not the distance between the remaining extreme cuts.','Sort and include both stick endpoints.'],'Hard',rec_time='O(3^c)',rec_space='O(c)')

add(51,'Burst Balloons','Partition DP','Choose the last action','Given non-negative balloon values, bursting a balloon earns left × value × right using its current neighbors. Missing outside neighbors have value 1. Burst all balloons and maximize coins.',
    ['Choosing the first balloon leaves neighbors that depend on the future burst order, so the two sides are not independent. Choose the last balloon of an interval instead.','When k is last, the interval’s outside neighbors are still present. Its reward is fixed: nums[i − 1] × nums[k] × nums[j + 1].','All other balloons in the left and right intervals can be burst independently first. Add their optima and try each possible last balloon.'],
    'f(i, j) is the maximum reward for removing balloons i through j while outside neighbors remain.',['i','j'],'if i > j:\n    return 0',
    'return max(f(i, k - 1) + f(k + 1, j) + nums[i - 1] * nums[k] * nums[j + 1]\n           for k in range(i, j + 1))',
    ['for i in range(n, 0, -1):','for j in range(i, n + 1):'],'f(1, n)','nums','nums = [1] + list(nums) + [1]\nn = len(nums) - 2',{'nums':[3,1,5,8]},167,'O(n³)','O(n²)',
    'values = [1] + list(nums) + [1]\nn = len(nums)\ndp = [[0] * (n + 2) for _ in range(n + 2)]\nfor length in range(1, n + 1):\n    for i in range(1, n - length + 2):\n        j = i + length - 1\n        dp[i][j] = max(dp[i][k - 1] + dp[k + 1][j] + values[i - 1] * values[k] * values[j + 1]\n                       for k in range(i, j + 1))\nreturn dp[1][n]',
    'O(n³) time and O(n²) space. The full interval dependency structure prevents a simple rolling-row reduction.',
    ['When first-action choices entangle subproblems, try the last action.','Outside interval neighbors are held fixed while solving that interval.','Pad with 1 at both boundaries, not zero.'],'Hard',rec_time='O(3^n)')

bool_body='counts = [0, 0]\nfor k in range(i + 1, j, 2):\n    left, right = f(i, k - 1), f(k + 1, j)\n    for a in (0, 1):\n        for b in (0, 1):\n            result = (a & b) if expression[k] == "&" else (a | b) if expression[k] == "|" else (a ^ b)\n            counts[result] += left[a] * right[b]\nreturn tuple(counts)'
add(52,'Boolean Parenthesization','Partition DP','Count outcomes across a split','Given a valid nonempty expression alternating T/F operands and &, |, or ^ operators, count full parenthesizations that evaluate to true. Return an exact integer; ^ means XOR.',
    ['Choose the final operator. Count how many left and right parenthesizations evaluate to false and true.','Each pair of left/right outcomes contributes the product of their counts. Use the operator’s truth table to route that product into the true or false bucket.','Storing both outcome counts in one state makes all truth-table cases explicit and avoids repeatedly deriving separate formulas.'],
    'f(i, j) returns (false_count, true_count) for expression[i:j+1].',['i','j'],'if i == j:\n    return (int(expression[i] == "F"), int(expression[i] == "T"))',bool_body,
    ['for i in range(n - 1, -1, -2):','for j in range(i, n, 2):'],'f(0, n - 1)[1]','expression','n = len(expression)',{'expression':'T|T&F^T'},4,'O(n³)','O(n²)',
    'n = len(expression)\ndp = {}\nfor i in range(0, n, 2):\n    dp[i, i] = (int(expression[i] == "F"), int(expression[i] == "T"))\nfor length in range(3, n + 1, 2):\n    for i in range(0, n - length + 1, 2):\n        j = i + length - 1\n        counts = [0, 0]\n        for k in range(i + 1, j, 2):\n            for a in (0, 1):\n                for b in (0, 1):\n                    result = (a & b) if expression[k] == "&" else (a | b) if expression[k] == "|" else (a ^ b)\n                    counts[result] += dp[i, k - 1][a] * dp[k + 1, j][b]\n        dp[i, j] = tuple(counts)\nreturn dp[0, n - 1][1]',
    'Both outcome counts require O(n²) table space and O(n³) time. Rolling rows are not applicable to arbitrary interval splits.',
    ['Multiply independent left/right counts, then add across alternatives.','Split only at operator indices.','Some judge variants require a modulus such as 1003 or 10^9+7; use the exact specification instead of assuming one.'],'Hard',rec_time='O(3^n)')

pal_setup='n = len(s)\npalindrome = [[False] * n for _ in range(n)]\nfor i in range(n - 1, -1, -1):\n    for j in range(i, n):\n        palindrome[i][j] = s[i] == s[j] and (j - i < 2 or palindrome[i + 1][j - 1])'
add(53,'Palindrome Partitioning II','Partition DP','Choose the next valid block','Split s into contiguous palindromic substrings and return the fewest cuts between them. Empty input needs zero cuts.',
    ['Try the endpoint of the first palindrome. Once that block is fixed, the suffix is an independent subproblem. Minimize the number of blocks.','Precompute which substrings are palindromes in O(n²). Testing every substring by slicing and reversing inside the DP would add another factor.','The answer counts cuts, while the recurrence counts blocks. For a nonempty string subtract one; an empty string is handled separately.'],
    'f(i) is the minimum number of palindrome blocks covering s[i:].',['i'],'if i == n:\n    return 0',
    'return 1 + min(f(j + 1) for j in range(i, n) if palindrome[i][j])',
    ['for i in range(n, -1, -1):'],'max(0, f(0) - 1)','s',pal_setup,{'s':'aab'},1,'O(n²)','O(n²)',
    'n = len(s)\ncuts = list(range(-1, n))\nfor center in range(n):\n    left = right = center\n    while left >= 0 and right < n and s[left] == s[right]:\n        cuts[right + 1] = min(cuts[right + 1], cuts[left] + 1)\n        left, right = left - 1, right + 1\n    left, right = center, center + 1\n    while left >= 0 and right < n and s[left] == s[right]:\n        cuts[right + 1] = min(cuts[right + 1], cuts[left] + 1)\n        left, right = left - 1, right + 1\nreturn max(0, cuts[n])',
    'Expanding palindromes around centers updates prefix cut counts in O(n²) time and O(n) space. All predecessor prefixes have earlier centers, so their best cuts are ready.',
    ['A valid next block plus an optimal suffix is partition DP.','Do not confuse number of blocks with number of cuts.','Precomputation memory is part of auxiliary space even when f has only one index.'],'Hard',rec_time='O(2^n + n²)')

add(54,'Partition Array for Maximum Sum','Partition DP','Bounded block choice','Partition nums into contiguous blocks of length at most k ≥ 1. Replace every value in each block with that block’s maximum. Return the largest possible total sum. Empty input returns 0.',
    ['At index i, try every legal end of the next block. Its contribution is block length times block maximum.','Maintain the maximum incrementally as the end moves, so evaluating all k choices costs O(k), not O(k²).','After choosing that block, add the optimum suffix starting just after it. A ring buffer needs only the next k suffix values.'],
    'f(i) is the maximum transformed sum for the suffix nums[i:].',['i'],'if i == n:\n    return 0',
    'best, maximum = -float("inf"), -float("inf")\nfor j in range(i, min(n, i + k)):\n    maximum = max(maximum, nums[j])\n    best = max(best, maximum * (j - i + 1) + f(j + 1))\nreturn best',
    ['for i in range(n, -1, -1):'],'f(0)','nums, k','n = len(nums)',{'nums':[1,15,7,9,2,5,10],'k':3},84,'O(nk)','O(n)',
    'n = len(nums)\nwidth = min(k, n) + 1\nrecent = [0] * width\nfor i in range(n - 1, -1, -1):\n    best = maximum = -float("inf")\n    for j in range(i, min(n, i + k)):\n        maximum = max(maximum, nums[j])\n        best = max(best, maximum * (j - i + 1) + recent[(j + 1) % width])\n    recent[i % width] = best\nreturn recent[0]',
    'A ring of the next min(k, n) + 1 answers gives O(nk) time and O(min(k,n)) space.',
    ['Choose a block boundary rather than choosing individual elements.','Keep a running maximum while extending the block.','For negative inputs initialize best with −infinity, not zero.'])

histogram='def area(heights):\n    stack = []\n    best = 0\n    for i in range(len(heights) + 1):\n        height = heights[i] if i < len(heights) else 0\n        while stack and heights[stack[-1]] > height:\n            h = heights[stack.pop()]\n            left = stack[-1] if stack else -1\n            best = max(best, h * (i - left - 1))\n        stack.append(i)\n    return best'
add(55,'Maximal Rectangle','Rectangles','Histogram heights + stack','Given a nonempty rectangular matrix of numeric 0s and 1s, return the largest area of an all-ones axis-aligned rectangle.',
    ['Treat each row as the bottom of a histogram: its column heights count consecutive ones ending on that row. A zero resets its column to zero.','Every all-ones rectangle has some bottom row, so take the best histogram rectangle across all rows. The height recurrence is DP; the histogram solver is a monotonic stack.','When a shorter bar appears, pop taller bars. Their maximal right boundary is now known, and the remaining stack top gives the left boundary. Each bar is pushed and popped once.'],
    'f(r, c) is the consecutive-one height at column c ending in row r.',['r','c'],'if r < 0:\n    return 0',
    'return 1 + f(r - 1, c) if matrix[r][c] == 1 else 0',
    ['for r in range(m):','for c in range(n):'],'max(area([f(r, c) for c in range(n)]) for r in range(m))','matrix','m, n = len(matrix), len(matrix[0])\n'+histogram,{'matrix':[[1,0,1,0,0],[1,0,1,1,1],[1,1,1,1,1],[1,0,0,1,0]]},6,'O(mn)','O(mn)',
    histogram+'\nheights = [0] * len(matrix[0])\nbest = 0\nfor row in matrix:\n    for c, value in enumerate(row):\n        heights[c] = heights[c] + 1 if value == 1 else 0\n    best = max(best, area(heights))\nreturn best',
    'Rolling histogram heights plus a monotonic stack: O(mn) time and O(n) space. There is no benefit to forcing the histogram portion into a recursive DP.',
    ['Separate the height DP from the largest-histogram-rectangle calculation.','Area equals popped height times the width between smaller neighbors.','This version uses numeric 1; convert string-valued judge inputs or compare against "1".'],'Hard',rec_time='O(m²n)',rec_space='O(m+n)')

add(56,'Count Square Submatrices with All Ones','Rectangles','Largest square ending here','Given a nonempty rectangular numeric binary matrix, count all axis-aligned square submatrices containing only ones, including 1 × 1 squares.',
    ['For a one-valued cell to end a square of side k, the cells above, left, and diagonally above-left must each support a square of at least side k − 1.','Therefore the largest side length is one plus the minimum of those three answers. A zero cell contributes zero.','If the largest square ending here has side k, there is exactly one ending-here square of each size 1 through k. Sum the state values to count every square once.'],
    'f(r, c) is the largest all-ones square side length with bottom-right corner (r, c).',['r','c'],'if r < 0 or c < 0 or matrix[r][c] == 0:\n    return 0',
    'return 1 + min(f(r - 1, c), f(r, c - 1), f(r - 1, c - 1))',
    ['for r in range(m):','for c in range(n):'],'sum(f(r, c) for r in range(m) for c in range(n))','matrix','m, n = len(matrix), len(matrix[0])',{'matrix':[[0,1,1,1],[1,1,1,1],[0,1,1,1]]},15,'O(mn)','O(mn)',
    'dp = [0] * (len(matrix[0]) + 1)\nanswer = 0\nfor row in matrix:\n    diagonal = 0\n    for c, value in enumerate(row, 1):\n        above = dp[c]\n        dp[c] = 1 + min(above, dp[c - 1], diagonal) if value == 1 else 0\n        diagonal = above\n        answer += dp[c]\nreturn answer',
    'One row plus an old-diagonal scalar: O(mn) time, O(n) space.',
    ['The minimum of three supporting squares controls how far a square can expand.','Sum side lengths to count squares; take max and square it to get maximal-square area.','Reset zero cells even when the previous row held a positive value.'],rec_space='O(m+n)')

# Keep complexity labels beside the code, with full caveats in the analysis text.
OPT_BOUNDS={1:('O(n)','O(1)'),2:('O(n)','O(1)'),3:('O(n)','O(1)'),4:('O(nk)','O(min(k,n))'),5:('O(n)','O(1)'),6:('O(n)','O(1)'),7:('O(n)','O(1)'),8:('O(mn)','O(n)'),9:('O(mn)','O(n)'),10:('O(mn)','O(n)'),11:('O(n²)','O(n)'),12:('O(mn)','O(n)'),13:('O(mn²)','O(n²)'),14:('O(nT)','O(T)'),15:('O(nS)','O(S)'),16:('O(nS)','O(S)'),17:('O(nT)','O(T)'),18:('O(nS)','O(S)'),19:('O(nW)','O(W)'),20:('O(nA)','O(A)'),21:('O(nS)','O(S)'),22:('O(nA)','O(A)'),23:('O(nW)','O(W)'),24:('O(n²)','O(n)'),25:('O(mn)','O(n)'),26:('O(mn + L)','O(mn + L)'),27:('O(mn)','O(n)'),28:('O(n²)','O(n)'),29:('O(n²)','O(n)'),30:('O(mn)','O(n)'),31:('O(mn+m+n)','O(mn+m+n)'),32:('O(mn)','O(n)'),33:('O(mn)','O(n)'),34:('O(mn+m)','O(n)'),35:('O(n)','O(1)'),36:('O(n)','O(1)'),37:('O(n)','O(1)'),38:('O(n min(k,n))','O(min(k,n))'),39:('O(n)','O(1)'),40:('O(n)','O(1)'),41:('O(n log n)','O(n)'),42:('O(n log n)','O(n)'),43:('O(n log n)','O(n)'),44:('O(n²)','O(n)'),45:('O(nL²+n log n)','O(n+L)'),46:('O(n log n)','O(n)'),47:('O(n²)','O(n)'),48:('O(n³)','O(n²)'),49:('O(n³)','O(n²)'),50:('O(c³+c log c)','O(c²)'),51:('O(n³)','O(n²)'),52:('O(n³)','O(n²)'),53:('O(n²)','O(n)'),54:('O(nk)','O(min(k,n))'),55:('O(mn)','O(n)'),56:('O(mn)','O(n)')}
for lesson in LESSONS:
    if lesson['id']==12:
        lesson['opt']=lesson['opt'].replace('for cells in matrix[1:]:','for r in range(1, len(matrix)):\n    cells = matrix[r]')
        lesson['opt_note']='Use two rows and index the matrix without copying its rows. O(mn) time, O(n) auxiliary space.'

def indent(s,n=1):
    return textwrap.indent(s,'    '*n)

def make_codes(d):
    args=', '.join(d['state'])
    prefix='def solve('+d['params']+'):\n'
    setup=indent(d['setup'])+'\n' if d['setup'] else ''
    fn='def f('+args+'):\n'+indent(d['base']+'\n'+d['body'])
    rec=prefix+setup+indent(fn)+'\n'+indent('return '+d['result'])+'\n'
    memo='from functools import cache\n\n'+prefix+setup+indent('@cache\n'+fn)+'\n'+indent('return '+d['result'])+'\n'
    key=args+(',' if len(d['state'])==1 else '')
    getter='def value('+args+'):\n'+indent(d['base']+'\nreturn dp['+key+']')
    calc='def transition('+args+'):\n'+indent((d['base']+'\n'+d['body']).replace('f(', 'value('))
    tab=prefix+setup+indent('dp = {}\n'+getter+'\n\n'+calc)+'\n'
    for depth,loop in enumerate(d['order'],1):tab+=indent(loop,depth)+'\n'
    tab+=indent('dp['+key+'] = transition('+args+')',len(d['order'])+1)+'\n'
    tab+=indent('return '+d['result'].replace('f(', 'value('))+'\n'
    opt=prefix+indent(d['opt'])+'\n' if d['opt'] else tab
    return [rec,memo,tab,opt]

def create_trace(d):
    args=', '.join(d['state'])
    src='def build('+d['params']+'):\n'+(indent(d['setup'])+'\n' if d['setup'] else '')
    src+=indent('@trace\ndef f('+args+'):\n'+indent(d['base']+'\n'+d['body']))+'\n'+indent('return '+d['result'])
    events=[]; stack=[];cache={}
    def trace(fn):
        def wrapped(*key):
            if stack: stack[-1]['deps'].append(dict(key=list(key),value=cache.get(key)))
            if key in cache:return cache[key]
            event=dict(key=list(key),deps=[])
            stack.append(event)
            value=fn(*key)
            stack.pop();cache[key]=value
            event['value']=value
            for dep in event['deps']:dep['value']=cache[tuple(dep['key'])]
            events.append(event)
            return value
        return wrapped
    env={'trace':trace};exec(src,env)
    answer=env['build'](**d['example'])
    return events,answer

def main():
    public=[]
    for d in LESSONS:
        codes=make_codes(d)
        for i,code in enumerate(codes):
            env={};exec(code,env);got=env['solve'](**d['example'])
            assert got==d['expected'],(d['id'],d['title'],i,got,d['expected'])
        events,answer=create_trace(d)
        assert answer==d['expected'],(d['id'],'trace',answer)
        def safe(v):
            if isinstance(v,float) and abs(v)==float('inf'):return '∞' if v>0 else '−∞'
            if isinstance(v,list):return [safe(x) for x in v]
            if isinstance(v,dict):return {k:safe(x) for k,x in v.items()}
            if isinstance(v,tuple):return list(v)
            return v
        p={k:d[k] for k in ['id','title','category','pattern','statement','intuition','example','expected','time','space','opt_note','notes','difficulty','rec_time','rec_space','extra']}
        p.update(state=d['base'],definition=d['intuition'],stateNames=d['state'],codes=codes,trace=safe(events),stateMeaning=d.get('meaning',''),recurrence=d['body'],order=d['order'],optTime=OPT_BOUNDS[d['id']][0],optSpace=OPT_BOUNDS[d['id']][1])
        # The author-facing field 'state' stores parameter names; prose is retained separately below.
        p['recognize']=d['pattern']
        public.append(p)
    pathlib.Path('dist/curriculum.js').write_text('window.CURRICULUM = '+json.dumps(public,ensure_ascii=False)+';\n',encoding='utf-8')
    print(f'Validated {len(public)} lessons × 4 Python approaches and {sum(len(p["trace"]) for p in public)} trace states.')

if __name__=='__main__':main()

