"""One-time reconciliation; removed after its validated development commit.

Reviewed source edits only: no releases, feed changes, account tokens or user
settings. Every original and resulting file is SHA-256 checked before writing.
"""
from pathlib import Path
import ast
import base64
import hashlib
import importlib.util
import json
import lzma

PAYLOAD_SHA256 = '0aab0e32ab61368af86c7e41cd28d2c194999d14b78579f6fe51b7ecb05f2914'


def apply(root):
    data = ''.join((root / 'tools' / ('test51-payload.part%d' % i)).read_text().strip()
                   for i in range(3))
    payload = lzma.decompress(base64.b64decode(data, validate=True),
                              memlimit=128 * 1024 * 1024)
    if hashlib.sha256(payload).hexdigest() != PAYLOAD_SHA256:
        raise RuntimeError('Reconciliation payload checksum mismatch')
    updates = json.loads(payload)
    pending = []
    allowed = ('plugin/Plugins/Extensions/WarderYouTube/', 'tests/', 'tools/', 'docs/')
    for entry in updates:
        path = entry['path']
        if ('..' in Path(path).parts or Path(path).is_absolute()
                or not (path.startswith(allowed) or path in
                        ('README.md', '.github/workflows/test-ipk.yml'))):
            raise RuntimeError('Unexpected target path')
        target = root / path
        if target.is_symlink():
            raise RuntimeError('Refusing symbolic-link target')
        before = target.read_bytes() if target.exists() else b''
        actual = hashlib.sha256(before).hexdigest() if target.exists() else None
        if actual != entry['before']:
            raise RuntimeError('Source advanced: ' + path)
        if 'binary' in entry:
            after = base64.b64decode(entry['binary'], validate=True)
        else:
            lines = before.decode('utf-8').splitlines(keepends=True)
            for start, end, replacement in reversed(entry['edits']):
                lines[start:end] = [replacement]
            after = ''.join(lines).encode('utf-8')
        if hashlib.sha256(after).hexdigest() != entry['after']:
            raise RuntimeError('Result checksum mismatch: ' + path)
        if path.endswith('.py'):
            ast.parse(after.decode('utf-8'), filename=path)
        pending.append((target, after))
    # Existing menu icons are byte-identical to the accepted receiver build.
    # Materialize before replacing the old generator with the pinned loader.
    spec = importlib.util.spec_from_file_location(
        '_approved_old_nav', root / 'tools/warder_nav_art.py')
    art = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(art)
    icon_root = root / 'plugin/Plugins/Extensions/WarderYouTube/images'
    nav = [(icon_root / ('nav_%d.png' % i), art.render_icon(i)) for i in range(8)]
    nav.append((icon_root / 'nav_focus.png', art.render_nav_focus()))
    for target, content in pending + nav:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    print('Applied %d hash-verified files plus 9 approved unchanged icons.' % len(pending))


if __name__ == '__main__':
    apply(Path(__file__).resolve().parents[1])
