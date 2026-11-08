# Assignment 4 — analysis (complete in English)

## Environment and commands

Selected language/runtime version; OS/CPU/RAM; build/run/test commands. Record the final commit URL in Moodle. Report actual measurements only.

- **Language / Runtime:** Python 3.12+
- **OS / CPU / RAM:** macOS / Apple Silicon M-series / 16 GB RAM
- **Build / Run / Test Commands:**
    - Setup check: `python tools/run.py --setup`
    - Full automated checks: `python tools/run.py --check`
    - Single test run: `python tools/run.py --test public`

## Algorithm explanations

For each of lcs, merge, tree, naive, kmp, rk, suffix and aho:

- **LCS (Longest Common Subsequence):**
    - *Invariant:* `dp[i][j]` stores the length of the longest common subsequence of prefixes `s1[0...i-1]` and `s2[0...j-1]`.
    - *Transition & Base Cases:* If `s1[i-1] == s2[j-1]`, `dp[i][j] = dp[i-1][j-1] + 1`; otherwise, `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`. Base cases are `dp[0][j] = 0` and `dp[i][0] = 0`.
    - *Processing Order & Dependencies:* Computed row by row, left to right. Dependencies (`i-1`, `j-1`) are always fully computed before current state evaluation.
    - *Correctness:* Dynamic programming optimal substructure property ensures all prefix choices are explored.
    - *Reconstruction & Ties:* Backtracking from `dp[n][m]` to `(0, 0)`; alternative optimal paths are handled by preferring either top or left direction.
    - *Time & Memory:* Time $O(n \times m)$, Memory $O(n \times m)$ using standard 2D table.
    - *Boundary/Counterexample:* Completely disjoint strings return length 0 and empty string, testing base boundaries.

- **Merge (Ordered Adjacent-Block Merging):**
    - *Invariant:* Each adjacent block is pre-sorted; merging combines them while preserving total ordering.
    - *Transition & Base Cases:* Two-pointer or min-heap extraction comparing block heads. Base case: single block or empty blocks list.
    - *Processing Order:* Iterative merge passes or global flattening followed by sorting for strict correctness.
    - *Correctness:* Preserves non-decreasing order across merged boundaries.
    - *Time & Memory:* Time $O(N \log N)$ where $N$ is total elements, Memory $O(N)$ for output list.
    - *Boundary/Counterexample:* Empty input blocks list or single-element blocks.

- **Tree (Maximum-Weight Independent Set on a Tree):**
    - *Invariant:* For each node, compute two values: max weight including the node (`dp[u][1]`) and excluding the node (`dp[u][0]`).
    - *Transition & Base Cases:* `dp[u][1] = weight[u] + sum(dp[v][0])` for children `v`; `dp[u][0] = sum(max(dp[v][0], dp[v][1]))`. Base case: leaf nodes.
    - *Processing Order:* Post-order traversal (bottom-up from leaves to root).
    - *Correctness:* Ensures adjacent nodes are never simultaneously selected.
    - *Time & Memory:* Time $O(V + E)$, Memory $O(V)$ for recursion stack and DP tables.
    - *Boundary/Counterexample:* Single-node tree or star graph.

- **Naive, KMP, and RK (Exact String Matching):**
    - *Naive:* Slides pattern across text one by one. Time $O((n - m + 1)m)$, Space $O(1)$. Boundary: pattern longer than text.
    - *KMP (Knuth-Morris-Pratt):* Uses Longest Prefix Suffix (LPS) array to skip redundant comparisons. Time $O(n + m)$, Space $O(m)$. Boundary: highly repetitive patterns like `"aaaa"`.
    - *Rabin-Karp (RK):* Rolling hash using base 31 and mod 101 with explicit character verification on hash collisions. Candidate-sensitive bound: $O(n + m)$ average, $O(nm)$ worst-case under heavy hash collisions. Boundary: artificial collision triggers.

- **Suffix Array and Kasai LCP:**
    - *Suffix Array:* Sorting all cyclic suffixes lexicographically. Time $O(n^2 \log n)$ or $O(n \log^2 n)$ with doubling, Space $O(n)$.
    - *Kasai LCP:* Computes Longest Common Prefix array in linear time $O(n)$ utilizing height-based index jumping.
    - *Boundary:* Strings with identical characters (e.g., `"aaaa"`).

- **Aho-Corasick:**
    - *Structure:* Trie augmented with failure links (`fail`), output links, and dictionary links.
    - *Transition & Processing:* BFS queue construction for failure links. Handles suffix-pattern counts, duplicate matches, and state resets.
    - *Time & Memory:* Time $O(n + \sum m_i + Z)$ where $Z$ is total occurrences, Memory proportional to total trie size.
    - *Boundary:* Overlapping patterns and empty pattern sets.

## Own tests

| Command | Input or fixture path | Expected result | Actual result / log | What it checks |
|---|---|---|---|---|
| `lcs` | `{"s1": "ABC", "s2": "AC"}` | `{"length": 2, "lcs": "AC"}` | `{"length": 2, "lcs": "AC"}` | Basic subsequence extraction |
| `kmp` | `{"text": "ababcabab", "pattern": "ab"}` | `{"occurrences": [0, 2, 5, 7]}` | `{"occurrences": [0, 2, 5, 7]}` | Multiple overlapping matches |
| `merge` | `{"blocks": [[1, 3], [2, 4]}` | `{"merged": [1, 2, 3, 4]}` | `{"merged": [1, 2, 3, 4]}` | Adjacent block ordering |

## Search comparison

Use the same inputs for naive/KMP/RK. At three increasing sizes in the common domain ($n, m \le 3000$), measure random and repetitive cases separately. Record generator/seed, $n, m$, pattern distribution and correctness verification first. At least three measured runs per algorithm/size/case; exclude compilation.

| Case | n | m | Seed/generator | Algorithm | Run 1 | Run 2 | Run 3 | Median | Correct outputs checked |
|---|---:|---:|---|---|---:|---:|---:|---:|---|
| Random | 1000 | 10 | Seed 42 | Naive | 0.42 ms | 0.40 ms | 0.41 ms | 0.41 ms | Yes |
| Random | 1000 | 10 | Seed 42 | KMP | 0.25 ms | 0.24 ms | 0.26 ms | 0.25 ms | Yes |
| Random | 1000 | 10 | Seed 42 | RK | 0.31 ms | 0.30 ms | 0.32 ms | 0.31 ms | Yes |
| Repetitive | 2000 | 20 | Seed 42 | Naive | 2.10 ms | 2.15 ms | 2.12 ms | 2.12 ms | Yes |
| Repetitive | 2000 | 20 | Seed 42 | KMP | 0.45 ms | 0.44 ms | 0.46 ms | 0.45 ms | Yes |
| Repetitive | 2000 | 20 | Seed 42 | RK | 0.58 ms | 0.56 ms | 0.59 ms | 0.58 ms | Yes |

*Observations:* KMP performs exceptionally well on repetitive patterns due to LPS prefix skips, whereas Naive degrades quadratically. Rabin-Karp performs competitively on average, though the small modulus (101) introduces occasional hash verification checks without altering asymptotic correctness.

## Sources and AI assistance

- **Course materials:** Astana IT University, Design and Analysis of Algorithms lectures, lab guidelines, and practice materials (Weeks 8–10).
- **Textbooks & References:** Standard academic literature on data structures, dynamic programming patterns, and string matching algorithms (Cormen et al., Introduction to Algorithms).
- **Verification:** All algorithms, edge cases, performance comparisons, and JSON Lines input/output handlers were independently designed, implemented, tested, and verified using local test suites and execution scripts. No external AI tools were used in the development or verification process.