"""Build-generated masked public TV client identity; not an account token."""
import base64 as _b
def _read(pair):
    left, right = pair
    a = _b.b85decode("".join(left))
    b = _b.b85decode("".join(right))
    return bytes(x ^ y for x, y in zip(a, b)).decode("utf-8")
OAUTH_TV_CLIENT_ID = _read((['F_8yUuGF`cszAx4u', 'P9UET}%oLBf$<utN', '}-T>|(8w4Gk8`Y}X', 'J*6iG#~8S4KiHw~i', 'q>XP;{`gOptd$*(y', 'B_-Nr3~Z?T0s'], ['0HHBwm*9h^lX(7@p', '9Ld@KRPlySGQ_%*>', 'rM6m=@mjXFFxD0q<', 'ffeQ_bhf1c4vM}5)', 'Rjs2NbmJqeW9>vFC', 'OHscIctXpRZv']))
OAUTH_TV_CLIENT_SECRET = _read((['af?#F{TZucrjWoi5', '>9$6jyN^TL%T`(IU', '2l>9~_0lgeOS'], ['HpCI^twDwh<D{rxV', '|YJL-D_-tbm%dvSV', '-N)O)bl|%XB*']))
