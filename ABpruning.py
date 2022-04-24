import math

pinfi = math.inf
ninfi = -math.inf


def ab_search(game, state):

    # Which player move next?
    player = game.toMove(state)
    value, move = maxValue(game, state, ninfi, pinfi)
    return move


def maxValue(game, state, alpha, beta):
    if game.isTerminal(state):
        return game.utility(state, player), None
    v = ninfi
    for a in game.actions(state):
        v2, a2 = minValue(game, game.result(state, a), alpha, beta)
        if v2 > v:
            v, move = v2, a
            alpha = max(alpha, v)
        if v >= beta:
            return v, move
    return v, move


def minValue(game, state, alpha, beta):
    if game.isTerminal(state):
        return game.utility(state, player), None
    v = pinfi
    for a in game.actions(state):
        v2, a2 = max(game, game.result(state, a), alpha, beta)
        if v2 < v:
            v, move = v2, a2
            beta = min(beta, v)
        if v <= alpha:
            return v, move
    return v, move
