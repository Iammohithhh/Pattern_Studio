import json, pathlib, difflib
root=pathlib.Path('content/reference')
catalog=[p for p in json.loads((root/'catalog.json').read_text(encoding='utf-8-sig')) if p.get('neetcode150')]
tree=json.loads((root/'tree.json').read_text(encoding='utf-8-sig'))
articles={pathlib.PurePosixPath(p['path']).stem:p['path'] for p in tree['tree'] if p['path'].startswith('articles/') and p['path'].endswith('.md')}
aliases={'contains-duplicate':'duplicate-integer','valid-anagram':'is-anagram','two-sum':'two-integer-sum','group-anagrams':'anagram-groups','two-sum-ii-input-array-is-sorted':'two-integer-sum-ii'}
aliases.update(dict(line.split('=') for line in '''top-k-frequent-elements=top-k-elements-in-list
product-of-array-except-self=products-of-array-discluding-self
encode-and-decode-strings=string-encode-and-decode
valid-palindrome=is-palindrome
3sum=three-integer-sum
container-with-most-water=max-water-container
best-time-to-buy-and-sell-stock=buy-and-sell-crypto
longest-substring-without-repeating-characters=longest-substring-without-duplicates
longest-repeating-character-replacement=longest-repeating-substring-with-replacement
permutation-in-string=permutation-string
minimum-window-substring=minimum-window-with-characters
valid-parentheses=validate-parentheses
min-stack=minimum-stack
search-a-2d-matrix=search-2d-matrix
koko-eating-bananas=eating-bananas
search-in-rotated-sorted-array=find-target-in-rotated-sorted-array
reverse-linked-list=reverse-a-linked-list
merge-two-sorted-lists=merge-two-sorted-linked-lists
reorder-list=reorder-linked-list
remove-nth-node-from-end-of-list=remove-node-from-end-of-linked-list
copy-list-with-random-pointer=copy-linked-list-with-random-pointer
linked-list-cycle=linked-list-cycle-detection
find-the-duplicate-number=find-duplicate-integer
merge-k-sorted-lists=merge-k-sorted-linked-lists
invert-binary-tree=invert-a-binary-tree
maximum-depth-of-binary-tree=depth-of-binary-tree
diameter-of-binary-tree=binary-tree-diameter
same-tree=same-binary-tree
subtree-of-another-tree=subtree-of-a-binary-tree
lowest-common-ancestor-of-a-binary-search-tree=lowest-common-ancestor-in-binary-search-tree
binary-tree-level-order-traversal=level-order-traversal-of-binary-tree
validate-binary-search-tree=valid-binary-search-tree
kth-smallest-element-in-a-bst=kth-smallest-integer-in-bst
construct-binary-tree-from-preorder-and-inorder-traversal=binary-tree-from-preorder-and-inorder-traversal
implement-trie-prefix-tree=implement-prefix-tree
design-add-and-search-words-data-structure=design-word-search-data-structure
word-search-ii=search-for-word-ii
kth-largest-element-in-a-stream=kth-largest-integer-in-a-stream
task-scheduler=task-scheduling
design-twitter=design-twitter-feed
find-median-from-data-stream=find-median-in-a-data-stream
combination-sum=combination-target-sum
combination-sum-ii=combination-target-sum-ii
word-search=search-for-word
letter-combinations-of-a-phone-number=combinations-of-a-phone-number
number-of-islands=count-number-of-islands
rotting-oranges=rotting-fruit
walls-and-gates=islands-and-treasure
number-of-connected-components-in-an-undirected-graph=count-connected-components
graph-valid-tree=valid-tree
reconstruct-itinerary=reconstruct-flight-path
min-cost-to-connect-all-points=min-cost-to-connect-points
alien-dictionary=foreign-dictionary
cheapest-flights-within-k-stops=cheapest-flight-path
unique-paths=count-paths
best-time-to-buy-and-sell-stock-with-cooldown=buy-and-sell-crypto-with-cooldown
longest-increasing-path-in-a-matrix=longest-increasing-path-in-matrix
distinct-subsequences=count-subsequences
merge-triplets-to-form-target-triplet=merge-triplets-to-form-target
insert-interval=insert-new-interval
meeting-rooms=meeting-schedule
meeting-rooms-ii=meeting-schedule-ii
minimum-interval-to-include-each-query=minimum-interval-including-query
rotate-image=rotate-matrix
set-matrix-zeroes=set-zeroes-in-matrix
happy-number=non-cyclical-number
powx-n=pow-x-n
detect-squares=count-squares
number-of-1-bits=number-of-one-bits'''.splitlines()))
mapping={}
for p in catalog:
    slug=p['link'].strip('/')
    name=aliases.get(slug,slug)
    if name in articles:mapping[p['code']]=articles[name]
    else:print(p['code'],':',difflib.get_close_matches(name,articles,n=3,cutoff=.38))
(root/'article-map.json').write_text(json.dumps(mapping,indent=2))
print('Matched',len(mapping),'of',len(catalog),'at commit',tree['sha'])
if __name__=='__main__' and len(mapping)==150:
    import concurrent.futures,urllib.request
    folder=root/'articles';folder.mkdir(exist_ok=True)
    def fetch(item):
        code,path=item;dest=folder/(code+'.md')
        if not dest.exists():
            dest.write_bytes(urllib.request.urlopen('https://raw.githubusercontent.com/neetcode-gh/leetcode/'+tree['sha']+'/'+path,timeout=40).read())
        return code,dest.stat().st_size
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        sizes=list(pool.map(fetch,mapping.items()))
    print('Fetched',len(sizes),'licensed articles;',sum(s for _,s in sizes),'bytes')
