#!/usr/bin/env python3
"""Copy the tested payload into an absent/empty directory, preserving user data."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    source=Path(__file__).resolve().parent.parent/'assets/deployment'
    target=args.output.expanduser().resolve()
    if target==source or source in target.parents or target in source.parents:
        parser.error('Choose a directory outside the skill payload.')
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        parser.error('Destination must be absent or empty; existing data was not modified.')
    manifest=json.loads((source/'vendor/upstream-manifest.json').read_text())
    wheel=source/'vendor'/manifest['sglang_wheel']['name']
    if hashlib.sha256(wheel.read_bytes()).hexdigest()!=manifest['sglang_wheel']['sha256']:
        parser.error('Vendored SGLang wheel checksum mismatch.')
    shutil.copytree(source,target,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.DS_Store'))
    print(json.dumps({'prepared':str(target),'model_revision':manifest['model_revision']}))

if __name__=='__main__':main()
