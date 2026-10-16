#!/usr/bin/env python3
"""Check UNSAT only through an external trusted DRAT checker; no cert => no claim."""
import argparse, subprocess, shutil, sys
p=argparse.ArgumentParser();p.add_argument('cnf');p.add_argument('drat')
a=p.parse_args()
checker=shutil.which('drat-trim')
if checker is None:
    sys.exit('No drat-trim installed: CANNOT certify UNSAT. No UNSAT claim is made.')
res=subprocess.run([checker,a.cnf,a.drat],check=False,capture_output=True,text=True)
print(res.stdout)
if res.returncode!=0:
    sys.exit('DRAT verification FAILED (no UNSAT certificate)')
print('DRAT verification succeeded')
