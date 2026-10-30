def eval_rpn(tokens: list[str]) -> int:
    st: list[int] = []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            if len(st) < 2:
                raise ValueError("stack underflow")
            b, a = st.pop(), st.pop()
            if t == "+":
                st.append(a + b)
            elif t == "-":
                st.append(a - b)
            elif t == "*":
                st.append(a * b)
            else:
                if b == 0:
                    raise ZeroDivisionError("division by zero")
                q = abs(a) // abs(b)
                st.append(q if (a >= 0) == (b >= 0) else -q)
        elif t == "neg":
            if not st:
                raise ValueError("stack underflow")
            st.append(-st.pop())
        else:
            try:
                st.append(int(t))
            except ValueError:
                raise ValueError(f"bad token {t!r}") from None
    if len(st) != 1:
        raise ValueError("malformed expression")
    return st[0]
