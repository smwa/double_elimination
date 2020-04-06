from double_elimination import Tournament as DoubleEliminationTournament

def printMatches(matches):
    print("Active Matches:")
    for match in matches:
        if match.is_ready_to_start():
            print("\t{} vs {}".format(*[p.get_competitor()
                                        for p in match.get_participants()]))


def add_win(det, competitor):
    det.add_win(competitor)


def checkActiveMatches(det, competitorPairs):
    matches = det.get_active_matches()
    if len(competitorPairs) != len(matches):
        printMatches(matches)
        print(competitorPairs)
        raise Exception("Invalid number of competitors: {} vs {}".format(
            len(matches), len(competitorPairs)))
    for match in matches:
        inMatches = False
        for competitorPair in competitorPairs:
            participants = match.get_participants()
            if competitorPair[0] == participants[0].get_competitor():
                if competitorPair[1] == participants[1].get_competitor():
                    inMatches = True
            elif competitorPair[0] == participants[1].get_competitor():
                if competitorPair[1] == participants[0].get_competitor():
                    inMatches = True
        if not inMatches:
            printMatches(matches)
            print(competitorPairs)
            raise Exception("Wrong matches")

def rangeBase1(length):
    return [i + 1 for i in range(length)]

if __name__ == '__main__':

    # 0 competitors
    try:
        DoubleEliminationTournament([])
        raise Exception('Expected error')
    except AssertionError:
        pass

    # 1 competitor
    try:
        DoubleEliminationTournament([1])
        raise Exception('Expected error')
    except AssertionError:
        pass

    # 2 competitors
    det = DoubleEliminationTournament(rangeBase1(2))
    checkActiveMatches(det, [[1, 2]])
    add_win(det, 1)
    checkActiveMatches(det, [[1, 2]])
    add_win(det, 2)
    checkActiveMatches(det, [])

    # 3 competitors
    det = DoubleEliminationTournament(rangeBase1(3))
    checkActiveMatches(det, [[2, 3]])
    add_win(det, 2)
    checkActiveMatches(det, [[2, 1]])
    add_win(det, 1)
    checkActiveMatches(det, [[2, 3]])
    add_win(det, 2)
    checkActiveMatches(det, [[2, 1]])
    add_win(det, 1)
    checkActiveMatches(det, [])

    # 4 competitors
    det = DoubleEliminationTournament(rangeBase1(4))
    checkActiveMatches(det, [[1, 4], [2, 3]])
    add_win(det, 2)
    checkActiveMatches(det, [[4, 1]])
    add_win(det, 1)
    checkActiveMatches(det, [[1, 2], [3, 4]])
    add_win(det, 4)
    checkActiveMatches(det, [[2, 1]])
    add_win(det, 1)
    checkActiveMatches(det, [[2, 4]])
    add_win(det, 4)
    checkActiveMatches(det, [[4, 1]])
    add_win(det, 1)
    checkActiveMatches(det, [])

    # 5 competitors
    det = DoubleEliminationTournament(rangeBase1(5))
    checkActiveMatches(det, [[2, 3], [4, 5]])
    add_win(det, 4)
    checkActiveMatches(det, [[4, 1], [2, 3]])
    add_win(det, 2)
    # checkActiveMatches(det, [[5, 3], [4, 1]])
    # add_win(det, 1)
    # checkActiveMatches(det, [[1, 2], [5, 3]])
    # add_win(det, 1)
    # checkActiveMatches(det, [[5, 3]])
    # add_win(det, 5)
    # checkActiveMatches(det, [[5, 4]])
    # add_win(det, 4)
    # checkActiveMatches(det, [[2, 4]])
    # add_win(det, 2)
    # checkActiveMatches(det, [[1, 2]])
    # add_win(det, 2)
    # checkActiveMatches(det, [])

    # 6 competitors
    det = DoubleEliminationTournament(rangeBase1(6))
    checkActiveMatches(det, [[4, 5], [3, 6]])
    add_win(det, 4)
    checkActiveMatches(det, [[3, 6], [4, 1]])
    add_win(det, 1)
    # checkActiveMatches(det, [[3, 6]])
    # add_win(det, 3)
    # checkActiveMatches(det, [[2,3],[4,6]])
    # add_win(det, 2)
    # checkActiveMatches(det, [[4,6],[3,5],[1,2]])
    # add_win(det, 2)
    # checkActiveMatches(det, [[4,6],[3,5]])
    # add_win(det, 6)
    # checkActiveMatches(det, [[3,5]])
    # add_win(det, 3)
    # checkActiveMatches(det, [[3,6]])
    # add_win(det, 3)
    # checkActiveMatches(det, [[1,3]])
    # add_win(det, 1)
    # checkActiveMatches(det, [[1,2]])
    # add_win(det, 1)
    # checkActiveMatches(det, [])

    # 7 competitors
    det = DoubleEliminationTournament(rangeBase1(7))
    checkActiveMatches(det, [[4, 5], [3, 6], [2, 7]])
    add_win(det, 4)
    checkActiveMatches(det, [[3, 6], [2, 7], [1, 4]])
    add_win(det, 1)
    checkActiveMatches(det, [[3, 6], [2, 7]])
    add_win(det, 3)
    # checkActiveMatches(det, [[2, 7]])
    # add_win(det, 2)
    # checkActiveMatches(det, [[6, 7], [2, 3]])
    # add_win(det, 3)
    # checkActiveMatches(det, [[6, 7], [5, 2], [1, 3]])
    # add_win(det, 1)
    # checkActiveMatches(det, [[6, 7], [5, 2]])
    # add_win(det, 2)
    # checkActiveMatches(det, [[6, 7]])
    # add_win(det, 7)
    # checkActiveMatches(det, [[4, 7]])
    # add_win(det, 4)
    # checkActiveMatches(det, [[2, 4]])
    # add_win(det, 2)
    # checkActiveMatches(det, [[2, 3]])
    # add_win(det, 2)
    # checkActiveMatches(det, [[1, 2]])
    # add_win(det, 2)
    # checkActiveMatches(det, [])

    # 8 competitors
    det = DoubleEliminationTournament(rangeBase1(8))
    checkActiveMatches(det, [[1, 8], [2, 7], [3, 6], [4, 5]])
    add_win(det, 3)
    checkActiveMatches(det, [[1, 8], [2, 7], [4, 5]])
    add_win(det, 7)
    checkActiveMatches(det, [[1, 8], [4, 5], [3, 7], [6,2]])
    add_win(det, 5)
    checkActiveMatches(det, [[1, 8], [3, 7], [6, 2]])
    add_win(det, 1)
    checkActiveMatches(det, [[3, 7], [6, 2], [1, 5], [4,8]])
    add_win(det, 5)
    checkActiveMatches(det, [[3, 7], [6, 2], [4, 8]])
    add_win(det, 3)
    checkActiveMatches(det, [[6, 2], [4, 8], [3, 5]])
    add_win(det, 3)
    checkActiveMatches(det, [[6, 2], [4, 8]])
    add_win(det, 4)
    checkActiveMatches(det, [[6, 2], [4, 7]])
    add_win(det, 4)
    checkActiveMatches(det, [[6, 2]])
    add_win(det, 2)
    checkActiveMatches(det, [[1, 2]])
    add_win(det, 1)
    checkActiveMatches(det, [[1, 4]])
    add_win(det, 4)
    checkActiveMatches(det, [[4, 5]])
    add_win(det, 5)
    checkActiveMatches(det, [[5,3]])
    add_win(det, 3)
    checkActiveMatches(det, [])
    if det.get_winners()[0] != 3:
        raise Exception("Invalid winner")

    print("Starting performance test")

    n = 1024
    det = DoubleEliminationTournament(range(n))
    matches = det.get_active_matches()
    while len(matches) > 0:
        for match in matches:
            det.add_win(match.get_participants()[0].get_competitor())
        matches = det.get_active_matches()

    print("Double elimination tests passed")
