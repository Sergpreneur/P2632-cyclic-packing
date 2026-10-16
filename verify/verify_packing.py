#!/usr/bin/env python3
"""Standalone explicit-shift verifier, independent of the orbit-resource matrix."""
import sys, json, itertools, hashlib, pathlib
N=31

def verify(blocks):
    seen_blocks=set(); seen_triples=set()
    for raw in blocks:
        b=tuple(sorted(raw))
        assert len(b)==5 and len(set(b))==5 and min(b)>=0 and max(b)<31,b
        for t in range(N):
            s=tuple(sorted((v+t)%N for v in b))
            if s in seen_blocks:
                raise ValueError('duplicate translated 5-set '+str(s))
            seen_blocks.add(s)
            for tri in itertools.combinations(s,3):
                if tri in seen_triples:
                    raise ValueError('duplicate translated triple '+str(tri))
                seen_triples.add(tri)
    assert len(seen_blocks)==31*len(blocks)
    assert len(seen_triples)==310*len(blocks)
    return {'base_blocks':len(blocks),'developed_blocks':len(seen_blocks),
            'distinct_triples':len(seen_triples),'unused_triples':4495-len(seen_triples),
            'status':'PASS'}

def main():
    inp=pathlib.Path(sys.argv[1])
    obj=json.loads(inp.read_text())
    blocks=obj['blocks'] if isinstance(obj,dict) else obj
    result=verify(blocks)
    result['file_sha256']=hashlib.sha256(inp.read_bytes()).hexdigest()
    print(json.dumps(result, indent=2))
if __name__=='__main__':main()
