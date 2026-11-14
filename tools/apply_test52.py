"""Apply locally tested test52 edits; removed after validated dev commit."""
from pathlib import Path
import ast
import base64
import hashlib
import json
import lzma

EXPECTED = 'a4a12d10ef1b5b3b4ba916a3dd65fbdb103b864db75c87695c86d028a4f25402'


def apply(root):
    encoded = (root / 'tools/test52.payload').read_text().strip()
    raw = lzma.decompress(base64.b64decode(encoded, validate=True),
                          memlimit=128 * 1024 * 1024)
    if hashlib.sha256(raw).hexdigest() != EXPECTED:
        raise RuntimeError('Payload checksum mismatch')
    pending = []
    for change in json.loads(raw):
        name = change['path']
        if (Path(name).is_absolute() or '..' in Path(name).parts
                or not name.startswith(('plugin/Plugins/Extensions/WarderYouTube/',
                                        'tests/', 'tools/', 'docs/'))):
            raise RuntimeError('Unexpected target')
        target = root / name
        if target.is_symlink():
            raise RuntimeError('Refusing symbolic link')
        old = target.read_bytes() if target.exists() else b''
        digest = hashlib.sha256(old).hexdigest() if target.exists() else None
        if digest != change['before']:
            raise RuntimeError('Source advanced: ' + name)
        lines = old.decode('utf-8').splitlines(keepends=True)
        for first, end, replacement in reversed(change['edits']):
            lines[first:end] = [replacement]
        new = ''.join(lines).encode('utf-8')
        if hashlib.sha256(new).hexdigest() != change['after']:
            raise RuntimeError('Result mismatch: ' + name)
        if name.endswith('.py'):
            ast.parse(new.decode('utf-8'), filename=name)
        pending.append((target, new))
    for target, content in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    print('Applied %d fully hash-verified files.' % len(pending))


if __name__ == '__main__':
    apply(Path(__file__).resolve().parents[1])
