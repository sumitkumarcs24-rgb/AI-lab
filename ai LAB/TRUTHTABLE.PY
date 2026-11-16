def PL_TRUE(sentence, model):
    return sentence(model)


def TT_CHECK_ALL(KB, alpha, symbols, model):
    if len(symbols) == 0:
        if PL_TRUE(KB, model):
            return PL_TRUE(alpha, model)
        else:
            return True
    else:
        P = symbols[0]
        rest = symbols[1:]

        return (TT_CHECK_ALL(KB, alpha, rest, model | {P: True}) and
                TT_CHECK_ALL(KB, alpha, rest, model | {P: False}))


def TT_ENTAILS(KB, alpha):
    symbols = ['P', 'Q', 'R']
    return TT_CHECK_ALL(KB, alpha, symbols, {})


def KB(model):
    P = model['P']
    Q = model['Q']
    R = model['R']

    return (not Q or P) and (not P or not Q) and (Q or R)


def alpha1(model):
    return model['R']


def alpha2(model):
    return not model['R'] or model['P']


def alpha3(model):
    return not model['Q'] or model['R']


print("P\tQ\tR\tQ->P\tP->~Q\tQVR\tKB")

for P in [False, True]:
    for Q in [False, True]:
        for R in [False, True]:
            model = {'P': P, 'Q': Q, 'R': R}

            q1 = not Q or P
            q2 = not P or not Q
            q3 = Q or R
            kb = KB(model)

            print(P, Q, R, q1, q2, q3, kb, sep="\t")

print("\nModels in which KB is TRUE:")

for P in [False, True]:
    for Q in [False, True]:
        for R in [False, True]:
            model = {'P': P, 'Q': Q, 'R': R}
            if KB(model):
                print(model)

print("\n(ii) KB entails R:", TT_ENTAILS(KB, alpha1))
print("(iii) KB entails R -> P:", TT_ENTAILS(KB, alpha2))
print("(iv) KB entails Q -> R:", TT_ENTAILS(KB, alpha3))