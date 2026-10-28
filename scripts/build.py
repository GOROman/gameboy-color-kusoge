#!/usr/bin/env python3
"""Build the tested standalone GBDK version from the shared native game source."""
import os
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parents[1]
src = (root / 'plugins/dash/engine/src/dash.c').read_text()
src = src.replace('#pragma bank 255\n', '').replace('#include "vm.h"', '')
src = src.replace('#include "dash_assets.h"', '#include "plugins/dash/engine/src/dash_assets.h"')
src = src.replace('void dash_duel(SCRIPT_CTX *THIS) OLDCALL BANKED {', 'void main(void) {')
src = src.replace('(void)THIS;', '')
src = '\n'.join(line.rstrip() for line in src.splitlines()) + '\n'
(root / 'standalone.c').write_text(src)
lcc = os.environ.get('GBDK_LCC') or shutil.which('lcc')
if not lcc:
    raise SystemExit('Set GBDK_LCC to the GBDK-2020 bin/lcc executable.')
(root / 'build').mkdir(exist_ok=True)
subprocess.run([lcc, '-Wm-yC', '-Wm-ynDASHDUEL', '-o', str(root / 'build/dash-duel.gbc'), str(root / 'standalone.c')], cwd=root, check=True)
print(root / 'build/dash-duel.gbc')
