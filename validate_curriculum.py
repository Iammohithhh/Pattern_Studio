"""Exercise edge cases, randomized inputs, and independently check key objectives."""
import random, itertools, functools, copy
from build_curriculum import LESSONS, make_codes
random.seed(42)
checks=0
def sub(seq, full):
    it=iter(full)
    return all(any(v==x for x in it) for v in seq)
def verify(d,inputs,expected=None):
    global checks
    results=[]
    for code in make_codes(d):
        env={};exec(code,env)
        results.append(env['solve'](**copy.deepcopy(inputs)))
        checks+=1
    if d['id'] in (26,31,42,44):
        assert len(set(map(len,results)))==1,(d['id'],inputs,results)
        for result in results:
            if d['id']==26: assert sub(result,inputs['a']) and sub(result,inputs['b'])
            if d['id']==31: assert sub(inputs['a'],result) and sub(inputs['b'],result)
            if d['id']==42: assert sub(result,inputs['nums']) and all(a<b for a,b in zip(result,result[1:]))
            if d['id']==44: assert all(a in inputs['nums'] for a in result) and all(b%a==0 for a,b in itertools.combinations(result,2))
    else:
        assert all(x==results[0] for x in results),(d['id'],inputs,results)
        if expected is not None:assert results[0]==expected,(d['id'],inputs,results,expected)
    return results[0]

for d in LESSONS:
    verify(d,d['example'])
    for _ in range(12):
        n=random.randint(0,6);a=[random.randrange(6) for _ in range(n)]
        i=d['id'];x=None;expected=None
        if i in (1,2):x={'n':n}
        elif i in (3,4):x={'heights':a or [0]};x.update({'k':random.randint(1,8)} if i==4 else {})
        elif i in (5,6,15,16,35,36,37,39,41,42,43,46,47,51):x={'prices' if i in (35,36,37,39) else 'nums':a}
        elif i==7:x={'points':[[random.randrange(-3,8) for _ in range(3)] for _ in range(n)]}
        elif i==8:x={'m':random.randint(1,4),'n':random.randint(1,4)}
        elif i in (9,10,12,13,55,56):x={'grid' if i in (9,10,13) else 'matrix':[[random.randrange(2 if i in (9,55,56) else 6) for _ in range(random.randint(1,1)+2)] for _ in range(random.randint(1,4))]}
        elif i==11:x={'triangle':[[random.randrange(-3,8) for _ in range(r+1)] for r in range(random.randint(1,5))]}
        elif i in (14,17,21):x={'nums':a,'target':random.randint(-3 if i==21 else 0,12)}
        elif i==18:x={'nums':a,'difference':random.randrange(12)}
        elif i in (19,23):x={'weights':[v+1 for v in a],'values':[random.randrange(-2,9) for _ in a],'capacity':random.randrange(9)}
        elif i in (20,22):x={'coins':sorted(set(v+1 for v in a)),'amount':random.randrange(9)}
        elif i==24:x={'prices':[random.randrange(-3,8) for _ in a]}
        elif i in (25,26,27,30,31,32,33):x={'a':''.join(random.choices('abc',k=n)),'b':''.join(random.choices('abc',k=random.randrange(6)))}
        elif i in (28,29,53):x={'s':''.join(random.choices('ab',k=n))}
        elif i==34:x={'text':''.join(random.choices('ab',k=n)),'pattern':''.join(random.choices('ab?*',k=random.randrange(6)))}
        elif i==38:x={'prices':a,'k':random.randrange(5)}
        elif i==40:x={'prices':a,'fee':random.randrange(4)}
        elif i==44:x={'nums':list(set(v+1 for v in a))}
        elif i==45:x={'words':[''.join(random.choices('ab',k=random.randint(1,4))) for _ in a]}
        elif i in (48,49):x={'dims':[random.randint(1,8) for _ in range(random.randint(2,6))]}
        elif i==50:x={'length':8,'cuts':random.sample(range(1,8),random.randrange(5))}
        elif i==52:x={'expression':''.join(random.choice('TF')+(random.choice('&|^') if j<n else '') for j in range(n+1))}
        elif i==54:x={'nums':[v-2 for v in a],'k':random.randint(1,8)}
        if i in (5,6):
            options=[sum(a[j] for j in range(n) if mask>>j&1) for mask in range(1<<n) if not(mask&(mask<<1)) and not(i==6 and n>1 and mask&1 and mask>>(n-1)&1)]
            expected=max(options)
        if i==14:expected=any(sum(a[j] for j in range(n) if mask>>j&1)==x['target'] for mask in range(1<<n))
        if i==17:expected=sum(sum(a[j] for j in range(n) if mask>>j&1)==x['target'] for mask in range(1<<n))
        if i==21:expected=sum(sum(v*sign for v,sign in zip(a,signs))==x['target'] for signs in itertools.product((-1,1),repeat=n))
        if i in (41,43,47):
            lengths=[]
            for mask in range(1,1<<n):
                seq=[a[j] for j in range(n) if mask>>j&1]
                if all(u<v for u,v in zip(seq,seq[1:])):lengths.append(len(seq))
            longest=max(lengths,default=0)
            expected=lengths.count(longest) if i==47 else longest
        if i==53:
            s=x['s']
            @functools.cache
            def pieces(start):
                if start==len(s):return 0
                return 1+min(pieces(end) for end in range(start+1,len(s)+1) if s[start:end]==s[start:end][::-1])
            expected=max(0,pieces(0)-1)
        if i in (55,56):
            matrix=x['matrix'];m=len(matrix);cols=len(matrix[0]);areas=[]
            for r in range(m):
                for c in range(cols):
                    for rr in range(r,m):
                        for cc in range(c,cols):
                            if all(matrix[y][z] for y in range(r,rr+1) for z in range(c,cc+1)):
                                if i==55 or rr-r==cc-c:areas.append((rr-r+1)*(cc-c+1))
            expected=max(areas,default=0) if i==55 else len(areas)
        verify(d,x,expected)
print(f'Passed {checks} Python executions across all 56 lessons, including randomized and empty/boundary cases.')
