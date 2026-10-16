#!/usr/bin/env python3
"""Static checks; does not pretend to replace the Lean compiler."""
from pathlib import Path
import json, re, tomllib, subprocess, sys
p=Path(__file__).resolve().parents[1]
settings=tomllib.loads((p/'lakefile.toml').read_text())
assert settings['name']=='p2632'
assert settings['defaultTargets']==['P2632','ResourceCertificate']
assert (p/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.35.0'
for path in [p/'P2632.lean',p/'ResourceCertificate.lean']:
    src=path.read_text()
    forbidden=[s for s in src.splitlines() if re.match(r'^\s*(?:sorry|axiom|unsafe\s+axiom)\b',s)]
    assert not forbidden,(path,forbidden)
    assert src.count('namespace P2632') == 1
    assert src.count('end P2632') == 1
assert 'theorem exists_twelve_orbit_packing' in (p/'P2632.lean').read_text()
assert 'theorem compact_resource_certificate' in (p/'ResourceCertificate.lean').read_text()
print('PASS: TOML and source structure checks (not Lean compilation)')
