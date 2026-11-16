def is_variable(x):
    return isinstance(x, str) and x.islower()


def occurs(var, term, subst):
    term = substitute(term, subst)

    if var == term:
        return True

    if isinstance(term, tuple):
        return any(occurs(var, t, subst) for t in term[1:])

    return False


def substitute(term, subst):
    if isinstance(term, str):
        while term in subst:
            term = subst[term]
        return term

    if isinstance(term, tuple):
        return (term[0],) + tuple(substitute(t, subst) for t in term[1:])

    return term


def unify(x, y, subst):
    x = substitute(x, subst)
    y = substitute(y, subst)

    if x == y:
        return subst

    if is_variable(x):
        if occurs(x, y, subst):
            return "FAILURE"
        subst[x] = y
        return subst

    if is_variable(y):
        if occurs(y, x, subst):
            return "FAILURE"
        subst[y] = x
        return subst

    if isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0] or len(x) != len(y):
            return "FAILURE"

        for a, b in zip(x[1:], y[1:]):
            subst = unify(a, b, subst)

            if subst == "FAILURE":
                return "FAILURE"

        return subst

    return "FAILURE"


def UNIFY(x, y):
    return unify(x, y, {})


print("Example 1:")
print(UNIFY(("Eats", "x", "Apple"),
            ("Eats", "Riya", "y")))

print("\nExample 2:")
print(UNIFY(("Knows", "John", "x"),
            ("Knows", "x", "Elizabeth")))

print("\nExample 3:")
print(UNIFY(("P", ("f", "a"), ("g", "Y")),
            ("P", "X", "X")))

print("\nExample 4:")
print(UNIFY(("Likes", "x", "Apple"),
            ("Eats", "Riya", "y")))