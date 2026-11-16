def unify(x, y, theta={}):
    if theta is None:
        return None
    if x == y:
        return theta
    if isinstance(x, str) and x.islower():
        theta[x] = y
        return theta
    if isinstance(y, str) and y.islower():
        theta[y] = x
        return theta
    if isinstance(x, tuple) and isinstance(y, tuple):
        if len(x) != len(y) or x[0] != y[0]:
            return None
        for a, b in zip(x[1:], y[1:]):
            theta = unify(a, b, theta)
            if theta is None:
                return None
        return theta
    return None


def substitute(expr, theta):
    if isinstance(expr, str):
        return theta.get(expr, expr)
    return (expr[0],) + tuple(substitute(x, theta) for x in expr[1:])


def fetch_all(premises, facts, theta={}):
    if not premises:
        return [theta]

    results = []
    first = substitute(premises[0], theta)

    for fact in facts:
        new_theta = unify(first, fact, theta.copy())

        if new_theta is not None:
            results.extend(fetch_all(premises[1:], facts, new_theta))

    return results


def forward_chaining(KB, query):
    facts = KB["facts"]
    rules = KB["rules"]

    while True:
        new = []

        for premises, conclusion in rules:
            substitutions = fetch_all(premises, facts)

            for theta in substitutions:
                result = substitute(conclusion, theta)

                if result not in facts and result not in new:
                    new.append(result)

                if unify(result, query, {}) is not None:
                    return True, facts + new

        if not new:
            return False, facts

        facts.extend(new)


KB = {
    "facts": [
        ("American", "Robert"),
        ("Owns", "A", "T1"),
        ("Missile", "T1"),
        ("Enemy", "A", "America")
    ],

    "rules": [
        ([("Missile", "x")],
         ("Weapon", "x")),

        ([("Missile", "x"), ("Owns", "A", "x")],
         ("Sells", "Robert", "x", "A")),

        ([("Enemy", "x", "America")],
         ("Hostile", "x")),

        ([("American", "p"), ("Weapon", "q"),
          ("Sells", "p", "q", "r"), ("Hostile", "r")],
         ("Criminal", "p"))
    ]
}

query = ("Criminal", "Robert")

result, facts = forward_chaining(KB, query)

print("Initial Facts:")
for fact in KB["facts"]:
    print(fact)

print("\nDerived Facts:")
for fact in facts[len(KB["facts"]):]:
    print(fact)

print("\nQuery:", query)
print("Result:", result)