"""Build the licensed NeetCode curriculum plus original teaching metadata."""
import ast, json, pathlib, re, textwrap
ROOT=pathlib.Path(__file__).parent
REF=ROOT/'content/reference'
CATALOG=[p for p in json.loads((REF/'catalog.json').read_text(encoding='utf-8-sig')) if p.get('neetcode150')]
MAP=json.loads((REF/'article-map.json').read_text())
COMMIT=json.loads((REF/'tree.json').read_text())['sha']

def plain(md):
    md=re.sub(r'```[\s\S]*?```','',md)
    md=re.sub(r'<[^>]*>|::[\w-]+','',md)
    return md.strip()

def parse(p):
    raw=(REF/'articles'/(p['code']+'.md')).read_text(encoding='utf-8-sig')
    sections=re.split(r'^## (?=\d+\.)',raw,flags=re.M)
    approaches=[]
    for section in sections[1:]:
        section=re.split(r'^## (?:Common Pitfalls|Prerequisites)',section,flags=re.M)[0]
        name=re.sub(r'^\d+\.\s*','',section.splitlines()[0]).strip()
        if p['code'].startswith('0238-') and name=='Division':continue
        if name=='Morris Traversal':continue
        if p['code'].startswith('0287-') and name in ('Sorting','Hash Set','Array','Negative Marking'):continue
        if p['code'].startswith('0070-') and name=='Math':continue
        py=re.findall(r'```python\s*\n([\s\S]*?)```',section)
        if not py:continue
        # Approach sections have a complete Python implementation; pitfalls are excluded.
        code=py[0].strip()+'\n'
        tree=ast.parse(code)
        forbidden={'exec','eval','open','compile','__import__','input','breakpoint'}
        optional_dependency=False
        for node in ast.walk(tree):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in forbidden:
                raise ValueError((p['code'],'unsafe call',node.func.id))
            if isinstance(node,(ast.Import,ast.ImportFrom)):
                names=[node.module] if isinstance(node,ast.ImportFrom) else [a.name for a in node.names]
                if any(n=='sortedcontainers' for n in names):optional_dependency=True
                assert all(n.split('.')[0] in {'typing','collections','heapq','math','bisect','functools','itertools','random','sys','operator','sortedcontainers'} for n in names),(p['code'],names)
        if optional_dependency:continue
        def part(heading):
            match=re.search(r'^### '+heading+r'\s*\n([\s\S]*?)(?=^### |::tabs-start|```|\Z)',section,re.M)
            return plain(match.group(1)) if match else ''
        complexity=re.search(r'### Time (?:&|and) Space Complexity\s*\n([\s\S]*?)(?=\n---|\Z)',section)
        complexity=plain(complexity.group(1)) if complexity else ''
        time=re.search(r'[Tt]ime complexity:\s*(.*)',complexity)
        space=re.search(r'[Ss]pace complexity:\s*(.*)',complexity)
        approaches.append(dict(title=name,code=code,intuition=part('Intuition'),algorithm=part('Algorithm'),complexity=complexity,time=time.group(1) if time else 'See analysis',space=space.group(1) if space else 'See analysis'))
    pre=re.search(r'^## Prerequisites\s*\n([\s\S]*?)(?=^## |\Z)',raw,re.M)
    pitfalls=re.search(r'^## Common Pitfalls\s*\n([\s\S]*)',raw,re.M)
    assert approaches,p['code']
    return dict(approaches=approaches,prerequisites=plain(pre.group(1)) if pre else '',pitfalls=plain(pitfalls.group(1)) if pitfalls else '')

def summary():
    for p in CATALOG:
        item=parse(p)
        print(p['code']+': '+' | '.join(str(i)+':'+a['title'] for i,a in enumerate(item['approaches'])))

PREFERRED={217:'Hash Set',36:'Hash Set (One Pass)',128:'Hash Set',150:'Stack',22:'Backtracking',739:'Stack',704:'Iterative Binary Search',138:'Hash Map (Two Pass)',146:'Doubly Linked List',226:'Depth First Search',104:'Recursive DFS',543:'Depth First Search',110:'Depth First Search',100:'Depth First Search',572:'Depth First Search (DFS)',98:'Depth First Search',230:'Iterative DFS (Optimal)',105:'Hash Map + Depth First Search',1046:'Heap',973:'Max Heap',215:'Quick Select',621:'Max-Heap',78:'Backtracking',46:'Backtracking',131:'Backtracking (DP)',51:'Backtracking (Hash Set)',200:'Breadth First Search',695:'Breadth First Search',130:'Breadth First Search',994:'Breadth First Search',210:"Topological Sort (Kahn's Algorithm)",127:'Breadth First Search - II',778:"Dijkstra's Algorithm",787:'Bellman Ford Algorithm',70:'Dynamic Programming (Space Optimized)',5:'Two Pointers',647:'Two Pointers',322:'Dynamic Programming (Bottom-Up)',152:"Kadane's Algorithm",139:'Dynamic Programming (Bottom-Up)',416:'Dynamic Programming (Space Optimized)',62:'Dynamic Programming (Space Optimized)',329:'Dynamic Programming (Top-Down)',53:"Kadane's Algorithm",1851:'Min Heap',191:'Bit Mask (Optimal)',190:'Bit Manipulation'}

def build():
    from neetcode_specs import SPECS
    from neetcode_runtime import prepare_code,run,verify
    import traceback
    lessons=[];failures=[];count=0
    for offset,p in enumerate(CATALOG):
        number=int(p['code'].split('-')[0]);spec=SPECS[number];parsed=parse(p);valid=[]
        for a in parsed['approaches']:
            code=prepare_code(a['code'])
            try:
                result,_=run(code,spec)
                assert verify(result,spec),f'expected {spec["expected"]!r}; got {result!r}'
                count+=1;valid.append({**a,'code':code})
            except Exception as error:
                failures.append(dict(problem=p['code'],approach=a['title'],error=str(error),detail=traceback.format_exc().splitlines()[-5:]))
        if not valid:continue
        choice=next((i for i,a in enumerate(valid) if a['title']==PREFERRED.get(number)),len(valid)-1)
        result,events=run(valid[choice]['code'],spec,trace=True)
        category='Backtracking' if number==22 else p['pattern']
        lessons.append(dict(id=1000+number,number=number,sequence=offset+1,track='neetcode',title=p['problem'],category=category,difficulty=p['difficulty'],statement=spec['statement'],example=spec['example'],expected=spec['expected'],cue=spec['cue'],pattern=valid[choice]['title'],stateMeaning=spec['cue'],approaches=valid,recommended=choice,trace=events,traceResult=result,prerequisites=parsed['prerequisites'],pitfalls=parsed['pitfalls'],source='https://github.com/neetcode-gh/leetcode/blob/'+COMMIT+'/'+MAP[p['code']],practice='https://neetcode.io/problems/'+pathlib.PurePosixPath(MAP[p['code']]).stem,runner=spec.get('runner','normal')))
    (ROOT/'content/neetcode-failures.json').write_text(json.dumps(failures,indent=2),encoding='utf-8')
    (ROOT/'dist/neetcode.js').write_text('window.NEETCODE = '+json.dumps(lessons,ensure_ascii=False)+';\n',encoding='utf-8')
    print(f'{len(lessons)}/150 lessons; {count} verified approaches; {len(failures)} approaches need review; {sum(len(p["trace"]) for p in lessons)} visual steps.')
    for f in failures:print(f['problem'],f['approach'],f['error'][:180])

if __name__=='__main__':
    import sys
    build() if '--build' in sys.argv else summary()
