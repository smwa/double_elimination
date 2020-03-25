from double_elimination import DoubleEliminationTournament

def printMatches(matches):
    print("Active Matches:")
    for match in matches:
        if match.isReadyToStart():
            print("\t{} vs {}".format(*[p.getCompetitor()
                                        for p in match.getParticipants()]))


def addWin(det, competitor):
    det.addWin(det.getActiveMatchForCompetitor(competitor), competitor)


def checkActiveMatches(det, competitorPairs):
    matches = det.getActiveMatches()
    if len(competitorPairs) != len(matches):
        printMatches(matches)
        print(competitorPairs)
        raise Exception("Invalid number of competitors: {} vs {}".format(
            len(matches), len(competitorPairs)))
    for match in matches:
        inMatches = False
        for competitorPair in competitorPairs:
            participants = match.getParticipants()
            if competitorPair[0] == participants[0].getCompetitor():
                if competitorPair[1] == participants[1].getCompetitor():
                    inMatches = True
            elif competitorPair[0] == participants[1].getCompetitor():
                if competitorPair[1] == participants[0].getCompetitor():
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
    addWin(det, 1)
    checkActiveMatches(det, [[1, 2]])
    addWin(det, 2)
    checkActiveMatches(det, [])

    # 3 competitors
    det = DoubleEliminationTournament(rangeBase1(3))
    checkActiveMatches(det, [[2, 3]])
    addWin(det, 2)
    checkActiveMatches(det, [[2, 1]])
    addWin(det, 1)
    checkActiveMatches(det, [[2, 3]])
    addWin(det, 2)
    checkActiveMatches(det, [[2, 1]])
    addWin(det, 1)
    checkActiveMatches(det, [])

    # 4 competitors
    det = DoubleEliminationTournament(rangeBase1(4))
    checkActiveMatches(det, [[1, 4], [2, 3]])
    addWin(det, 2)
    checkActiveMatches(det, [[4, 1]])
    addWin(det, 1)
    checkActiveMatches(det, [[1, 2], [3, 4]])
    addWin(det, 4)
    checkActiveMatches(det, [[2, 1]])
    addWin(det, 1)
    checkActiveMatches(det, [[2, 4]])
    addWin(det, 4)
    checkActiveMatches(det, [[4, 1]])
    addWin(det, 1)
    checkActiveMatches(det, [])

    # 5 competitors
    det = DoubleEliminationTournament(rangeBase1(5))
    checkActiveMatches(det, [[2, 3], [4, 5]])
    addWin(det, 4)
    checkActiveMatches(det, [[4, 1], [2, 3]])
    addWin(det, 2)
    checkActiveMatches(det, [[5, 3], [4, 1]])
    addWin(det, 1)
    checkActiveMatches(det, [[1, 2], [5, 3]])
    addWin(det, 1)
    checkActiveMatches(det, [[5, 3]])
    addWin(det, 5)
    checkActiveMatches(det, [[5, 4]])
    addWin(det, 4)
    checkActiveMatches(det, [[2, 4]])
    addWin(det, 2)
    checkActiveMatches(det, [[1, 2]])
    addWin(det, 2)
    checkActiveMatches(det, [])

    # 6 competitors
    det = DoubleEliminationTournament(rangeBase1(6))
    checkActiveMatches(det, [[4, 5], [3, 6]])
    addWin(det, 4)
    checkActiveMatches(det, [[3, 6], [4, 1]])
    addWin(det, 1)
    checkActiveMatches(det, [[3, 6]])
    addWin(det, 3)
    checkActiveMatches(det, [[2,3],[4,6]])
    addWin(det, 2)
    checkActiveMatches(det, [[4,6],[3,5],[1,2]])
    addWin(det, 2)
    checkActiveMatches(det, [[4,6],[3,5]])
    addWin(det, 6)
    checkActiveMatches(det, [[3,5]])
    addWin(det, 3)
    checkActiveMatches(det, [[3,6]])
    addWin(det, 3)
    checkActiveMatches(det, [[1,3]])
    addWin(det, 1)
    checkActiveMatches(det, [[1,2]])
    addWin(det, 1)
    checkActiveMatches(det, [])

    # 7 competitors
    det = DoubleEliminationTournament(rangeBase1(7))
    checkActiveMatches(det, [[4, 5], [3, 6], [2, 7]])
    addWin(det, 4)
    checkActiveMatches(det, [[3, 6], [2, 7], [1, 4]])
    addWin(det, 1)
    checkActiveMatches(det, [[3, 6], [2, 7]])
    addWin(det, 3)
    checkActiveMatches(det, [[2, 7]])
    addWin(det, 2)
    checkActiveMatches(det, [[6, 7], [2, 3]])
    addWin(det, 3)
    # checkActiveMatches(det, [[6, 7], [5, 2], [1, 3]])
    # addWin(det, 1)
    # checkActiveMatches(det, [[6, 7], [5, 2]])
    # addWin(det, 2)
    # checkActiveMatches(det, [[6, 7]])
    # addWin(det, 7)
    # checkActiveMatches(det, [[4, 7]])
    # addWin(det, 4)
    # checkActiveMatches(det, [[2, 4]])
    # addWin(det, 2)
    # checkActiveMatches(det, [[2, 3]])
    # addWin(det, 2)
    # checkActiveMatches(det, [[1, 2]])
    # addWin(det, 2)
    # checkActiveMatches(det, [])

    # 8 competitors
    det = DoubleEliminationTournament(rangeBase1(8))
    checkActiveMatches(det, [[1, 8], [2, 7], [3, 6], [4, 5]])
    addWin(det, 3)
    checkActiveMatches(det, [[1, 8], [2, 7], [4, 5]])
    addWin(det, 7)
    checkActiveMatches(det, [[1, 8], [4, 5], [3, 7], [6,2]])
    addWin(det, 5)
    checkActiveMatches(det, [[1, 8], [3, 7], [6, 2]])
    addWin(det, 1)
    checkActiveMatches(det, [[3, 7], [6, 2], [1, 5], [4,8]])
    addWin(det, 5)
    checkActiveMatches(det, [[3, 7], [6, 2], [4, 8]])
    addWin(det, 3)
    checkActiveMatches(det, [[6, 2], [4, 8], [3, 5]])
    addWin(det, 3)
    checkActiveMatches(det, [[6, 2], [4, 8]])
    addWin(det, 4)
    checkActiveMatches(det, [[6, 2], [4, 7]])
    addWin(det, 4)
    checkActiveMatches(det, [[6, 2]])
    addWin(det, 2)
    checkActiveMatches(det, [[1, 2]])
    addWin(det, 1)
    checkActiveMatches(det, [[1, 4]])
    addWin(det, 4)
    checkActiveMatches(det, [[4, 5]])
    addWin(det, 5)
    checkActiveMatches(det, [[5,3]])
    addWin(det, 3)
    checkActiveMatches(det, [])

    print("Starting performance test")

    n = 4096
    det = DoubleEliminationTournament(range(n))
    matches = det.getActiveMatches()
    while len(matches) > 0:
        for match in matches:
            det.addWin(match, match.getParticipants()[0].getCompetitor())
        matches = det.getActiveMatches()

    print("Double elimination tests passed")
