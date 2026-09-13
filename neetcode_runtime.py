"""Execute trusted, reviewed algorithm examples and record their real Python states."""
import ast, collections, copy, inspect, json, math, sys, typing

class ListNode:
    def __init__(self,val=0,next=None):self.val,self.next=val,next
class TreeNode:
    def __init__(self,val=0,left=None,right=None):self.val,self.left,self.right=val,left,right
class Node:
    def __init__(self,val=0,next=None,random=None,neighbors=None):
        self.val,self.next,self.random=val,next,random
        self.neighbors=neighbors if neighbors is not None else []
class Interval:
    def __init__(self,start,end):self.start,self.end=start,end

def linked(values):
    dummy=ListNode();tail=dummy
    for value in values:tail.next=ListNode(value);tail=tail.next
    return dummy.next
def tree(values):
    if not values or values[0] is None:return None
    root=TreeNode(values[0]);queue=collections.deque([root]);i=1
    while queue and i<len(values):
        node=queue.popleft()
        if values[i] is not None:node.left=TreeNode(values[i]);queue.append(node.left)
        i+=1
        if i<len(values) and values[i] is not None:node.right=TreeNode(values[i]);queue.append(node.right)
        i+=1
    return root
def tree_values(root):
    if root is None:return []
    answer=[];queue=collections.deque([root]);seen=set()
    while queue:
        node=queue.popleft()
        if node is None:answer.append(None);continue
        if id(node) in seen:raise ValueError('Cycle in tree output')
        seen.add(id(node));answer.append(node.val);queue.extend((node.left,node.right))
    while answer and answer[-1] is None:answer.pop()
    return answer
def list_values(head):
    values=[];seen=set()
    while head:
        if id(head) in seen:raise ValueError('Unexpected cycle in output list')
        seen.add(id(head));values.append(head.val);head=head.next
    return values
def find_node(root,value):
    if root is None:return None
    if root.val==value:return root
    return find_node(root.left,value) or find_node(root.right,value)

def prepare_code(code):
    parsed=ast.parse(code)
    names={node.id for node in ast.walk(parsed) if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Load)}
    imports=[]
    groups={'typing':['List','Optional','Dict','Set','Tuple','Deque','DefaultDict','Any'],
            'collections':['defaultdict','deque','Counter','OrderedDict'],
            'heapq':['heapify','heappush','heappop','heappushpop','heapreplace','nlargest','nsmallest'],
            'bisect':['bisect_left','bisect_right','insort'],
            'math':['ceil','floor','sqrt','inf','log2','comb'],
            'functools':['cache','lru_cache'],
            'itertools':['product','permutations','combinations','chain'],
            'random':['randint','randrange','choice']}
    for module,candidates in groups.items():
        used=[n for n in candidates if n in names]
        if used:imports.append('from '+module+' import '+', '.join(used))
    for module in ['collections','heapq','math','bisect','functools','random','itertools','sys']:
        if module in names:imports.append('import '+module)
    return '\n'.join(imports)+('\n\n' if imports else '')+code

def freeze(value,depth=0,seen=None):
    seen=set() if seen is None else seen
    if value is None or isinstance(value,(bool,int,str)):
        return value if not isinstance(value,str) or len(value)<180 else value[:177]+'…'
    if isinstance(value,float):return value if math.isfinite(value) else ('∞' if value>0 else '−∞')
    if depth>3:return '…'
    if isinstance(value,(list,tuple,collections.deque)):
        items=list(value);return [freeze(v,depth+1,seen.copy()) for v in items[:32]]+(['…'] if len(items)>32 else [])
    if isinstance(value,(set,frozenset)):return {'kind':'set','items':[freeze(v,depth+1,seen.copy()) for v in sorted(value,key=str)[:32]]}
    if isinstance(value,dict):return {'kind':'map','entries':[[str(k),freeze(v,depth+1,seen.copy())] for k,v in list(value.items())[:24]]}
    if hasattr(value,'val'):
        if id(value) in seen:return {'kind':'ref','value':value.val}
        seen.add(id(value))
        result={'kind':'node','value':value.val,'identity':id(value)}
        if hasattr(value,'left'):result.update(left=freeze(value.left,depth+1,seen.copy()),right=freeze(value.right,depth+1,seen.copy()))
        if hasattr(value,'next'):result['next']=freeze(value.next,depth+1,seen.copy())
        if hasattr(value,'neighbors'):result['neighbors']=[n.val for n in value.neighbors]
        if hasattr(value,'random'):result['random']=value.random.val if value.random else None
        return result
    if hasattr(value,'start') and hasattr(value,'end'):return [value.start,value.end]
    if hasattr(value,'__dict__') and not isinstance(value,(type,typing.TypeVar)):
        return {'kind':'object','fields':{k:freeze(v,depth+1,seen.copy()) for k,v in vars(value).items() if not k.startswith('__')}}
    return None

def run(code,spec,trace=False,limit=10000):
    filename='<lesson>'
    env={'ListNode':ListNode,'TreeNode':TreeNode,'Node':Node,'Interval':Interval}
    exec(compile(code,filename,'exec'),env)
    args=copy.deepcopy(spec['example']);runner=spec.get('runner','normal');events=[];calls=[];ticks=0
    def tracer(frame,event,arg):
        nonlocal ticks
        if frame.f_code.co_filename!=filename:return tracer
        ticks+=1
        if ticks>150000:raise RuntimeError('Example exceeded execution budget')
        if not trace:return tracer
        if event=='call':calls.append(frame.f_code.co_name)
        if event in ('line','return') and len(events)<limit:
            variables={k:freeze(v) for k,v in frame.f_locals.items() if not k.startswith('__') and not inspect.isfunction(v) and not isinstance(v,type)}
            if event=='return':variables['return']=freeze(arg)
            events.append(dict(line=frame.f_lineno,event=event,function=frame.f_code.co_name,stack=calls[-10:].copy(),variables=variables))
        if event=='return' and calls:calls.pop()
        return tracer
    if runner in ('linked','cycle'):
        for key in ['head','list1','list2','l1','l2']:
            if key in args:args[key]=linked(args[key])
        if 'lists' in args:args['lists']=[linked(v) for v in args['lists']]
        if runner=='cycle':
            pos=args.pop('pos');nodes=[];cur=args['head']
            while cur:nodes.append(cur);cur=cur.next
            if nodes and pos>=0:nodes[-1].next=nodes[pos]
    elif runner in ('tree','tree-codec'):
        for key in ['root','p','q','subRoot']:
            if key in args and isinstance(args[key],list):args[key]=tree(args[key])
        if spec.get('lca'):
            args['p']=find_node(args['root'],args['p']);args['q']=find_node(args['root'],args['q'])
    elif runner=='random-list':
        nodes=[Node(v) for v,_ in args['head']]
        for i,(_,r) in enumerate(args['head']):
            nodes[i].next=nodes[i+1] if i+1<len(nodes) else None
            nodes[i].random=nodes[r] if r is not None else None
        args['head']=nodes[0] if nodes else None
    elif runner=='graph':
        adjacent=args.pop('adjacency');nodes=[Node(i+1) for i in range(len(adjacent))]
        for node,links in zip(nodes,adjacent):node.neighbors=[nodes[i-1] for i in links]
        args['node']=nodes[0] if nodes else None
    if 'intervals' in args and '.start' in code:args['intervals']=[Interval(*v) for v in args['intervals']]
    sys.settrace(tracer)
    try:
        if runner=='design':
            cls=env.get(spec['className'])
            if cls is None and spec['className']=='Trie':cls=env.get('PrefixTree')
            if cls is None and spec['className']=='DetectSquares':cls=env.get('CountSquares')
            obj=cls(*(args[k] for k in spec.get('constructor',[])))
            result=[]
            for method,values in args['operations']:result.append(getattr(obj,method)(*values))
        elif runner in ('codec','tree-codec'):
            cls=env.get('Codec',env.get('Solution'));obj=cls()
            if runner=='codec':result=obj.decode(obj.encode(args['strings']))
            else:result=obj.deserialize(obj.serialize(args['root']))
        else:
            obj=env['Solution']()
            methods=[k for k,v in env['Solution'].__dict__.items() if callable(v) and not k.startswith('__')]
            method=spec.get('method',methods[0])
            result=getattr(obj,method)(*args.values())
            if spec.get('mutates'):result=args[spec['mutates']]
    finally:sys.settrace(None)
    if runner=='linked':result=list_values(result)
    elif runner=='tree-codec' or spec.get('resultTree'):result=tree_values(result)
    elif spec.get('lca'):result=result.val
    elif runner=='random-list':
        copied=[];cur=result
        while cur:copied.append(cur);cur=cur.next
        assert all(node not in nodes for node in copied),'Shallow copy detected'
        positions={id(node):i for i,node in enumerate(copied)}
        result=[[node.val,positions[id(node.random)] if node.random else None] for node in copied]
    elif runner=='graph':
        queue=collections.deque([result] if result else []);seen={};
        while queue:
            node=queue.popleft()
            if node.val in seen:continue
            assert node not in nodes,'Shallow graph copy detected'
            seen[node.val]=sorted(n.val for n in node.neighbors);queue.extend(node.neighbors)
        result=[seen[k] for k in sorted(seen)]
    if isinstance(result,(set,tuple)):result=list(result)
    return result,events

def verify(result,spec):
    expected=spec['expected'];mode=spec.get('compare')
    if mode=='groups':return sorted(sorted(v) for v in result)==sorted(sorted(v) for v in expected)
    if mode in ('sequences','coordinates'):return sorted(result)==sorted(expected)
    if mode=='unordered':return sorted(result)==sorted(expected)
    if mode=='palindrome':return len(result)==len(expected) and result==result[::-1] and result in spec['example']['s']
    if mode=='topological':
        n=spec['example']['numCourses']
        return sorted(result)==list(range(n)) and all(result.index(b)<result.index(a) for a,b in spec['example']['prerequisites'])
    if isinstance(result,float):return math.isclose(result,expected,rel_tol=1e-8)
    return result==expected
