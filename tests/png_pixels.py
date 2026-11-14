"""Minimal standard-library RGBA PNG unfiltering for fixture validation."""
def unfilter_rgba(data, width, height):
    stride = width * 4
    assert len(data) == (stride + 1) * height
    out = bytearray()
    previous = bytearray(stride)
    for y in range(height):
        start = y * (stride + 1)
        kind = data[start]
        row = bytearray(data[start+1:start+1+stride])
        for x in range(stride):
            a = row[x-4] if x >= 4 else 0
            b = previous[x]
            c = previous[x-4] if x >= 4 else 0
            if kind == 0: predictor = 0
            elif kind == 1: predictor = a
            elif kind == 2: predictor = b
            elif kind == 3: predictor = (a + b) // 2
            elif kind == 4:
                p = a + b - c
                pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                predictor = a if pa <= pb and pa <= pc else b if pb <= pc else c
            else: raise AssertionError("Invalid PNG filter")
            row[x] = (row[x] + predictor) & 255
        out.extend(row)
        previous = row
    return bytes(out)
