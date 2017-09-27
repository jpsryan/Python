import itertools

def BestOfSeven(SevenCards):
    TempResult = "Null"
    PrevTempResult = "Null"
    PlayOffResult = "Null"
    BestHand = "Null"


    # SevenCards[0], SevenCards[1], then check others 10 combinations per player
    CurHandToCheck3 = itertools.combinations(SevenCards[2:7],3)             # Contains tuples
    CurHandToCheck2 = list(CurHandToCheck3)                                  # Make it a list of tuples
    CurHandToCheck = [SevenCards[0], SevenCards[1], "Null", "Null", "Null"]

    for x in range(0,10):                               # Here we are checking the 10 combinations
        CurHandToCheck[2] = CurHandToCheck2[x][0]       # and looping until we return the best one
        CurHandToCheck[3] = CurHandToCheck2[x][1]
        CurHandToCheck[4] = CurHandToCheck2[x][2]
        if x == 0:
            PrevTempResult = Rank(CurHandToCheck)       # handtype, highcard1, highcard 2
            BestHand = CurHandToCheck

        TempResult = Rank(CurHandToCheck)
        PlayOffResult = Compare(PrevTempResult, TempResult)

        if PlayOffResult == "Hand2":
            PrevTempResult = TempResult
            BestHand = CurHandToCheck

    return BestHand, PrevTempResult

def Rank(Hand):                                         # Intake a single 5-card hand, return Hand type and
    HandType = ""                                       # high card(s)
    HighCard1 = 0
    HighCard2 = 0
    FlushResults = []
    StraightResults = []

    FlushResults = CheckFlush(Hand)
    StraightResults = CheckStraight(Hand)
    PairResults = CheckPairTripFullHouse(Hand)

    if FlushResults[0] == "Flush":
        if StraightResults[0] == "Straight":
            HandType = "StraightFlush"
            HighCard1 = StraightResults[1]
        else:
            HandType = "Flush"
            HighCard1 = FlushResults[1]

    if StraightResults[0] == "Straight" and FlushResults[0] == "NoFlush":
        HandType = "Straight"
        HighCard1 = StraightResults[1]


    if PairResults[0] == "FourOfAKind":
        HandType = "FourOfAKind"
        HighCard1 = PairResults[1]
    elif PairResults[0] == "FullHouse":
        HandType = "FourOfAKind"
        HighCard1 = PairResults[1]
        HighCard2 = PairResults[2]
    elif PairResults[0] == "Trips":
        HandType = "Trips"
        HighCard1 = PairResults[1]
    elif PairResults[0] == "TwoPair":
        HandType = "TwoPair"
        HighCard1 = PairResults[1]
        HighCard2 = PairResults[2]
    elif PairResults[0] == "OnePair":
        HandType = "OnePair"
        HighCard1 = PairResults[1]
    else:
        HandType = "HighCard"
        HighCard1 = PairResults[1]

    return HandType, HighCard1, HighCard2

def CheckPairTripFullHouse(FiveCards):
    Flaggo = False
    HighCard1 = 0
    HighCard2 = 0
    TripFlag = False
    HandType = "Null"
    Numba = []

    for x in range(0,5):
        Numba.append(FiveCards[x][0])                                   # Strip out card numbers into list Numba

    for x in range(2,15):
        if Numba.count(x) == 4:
            HighCard1 = x
            HandType = "FourOfAKind"
        elif Numba.count(x) == 3 and Flaggo is True:
            HighCard2 = HighCard1
            HighCard1 = x
            HandType = "FullHouse"
        elif Numba.count(x) == 3 and Flaggo is False:
            HighCard1 = x
            HandType = "Trips"
            TripFlag = True
        elif Numba.count(x) == 2 and Flaggo is True:
            HighCard2 = HighCard1
            HighCard1 = x
            HandType = "TwoPair"
        elif Numba.count(x) == 2 and Flaggo is False and TripFlag is True:
            HighCard2 = HighCard1
            HighCard1 = x
            HandType = "FullHouse"
        elif Numba.count(x) == 2 and Flaggo is False and TripFlag is False:
            HighCard1 = x
            HandType = "OnePair"
            Flaggo = True
        elif Numba.count(x) == 1 and HandType == "HighCard" and x > HighCard1:
            HighCard1 = x
        elif Numba.count(x) == 1 and HandType == "Null" and x > HighCard1:
            HighCard1 = x
            HandType = "HighCard"
        else:
            pass

    return HandType, HighCard1, HighCard2

def CheckFlush(FiveCards):

    HandType = "Null"
    Suits = ["Null"]
    Numba = ["Null"]
    HighCard = 0

    for x in range(0, 5):
        if x == 0:
            Suits[0] = FiveCards[x][1]
        else:
            Suits.append(FiveCards[x][1])  # Create string of suits
    for x in range(0, 5):
        if x == 0:
            Numba[0] = FiveCards[x][0]
        else:
            Numba.append(FiveCards[x][0])  # Create string of values

    for x in range(0, 5):
        if Suits.count("C") == 5:
            HandType = "Flush"
            HighCard = max(Numba)
        elif Suits.count("D") == 5:
            HandType = "Flush"
            HighCard = max(Numba)
        elif Suits.count("H") == 5:
            HandType = "Flush"
            HighCard = max(Numba)
        elif Suits.count("S") == 5:
            HandType = "Flush"
            HighCard = max(Numba)
        else:
            HandType = "NoFlush"

    return HandType, HighCard

def CheckStraight(FiveCards):
    Numba = ["Null"]
    HandType = "NoStraight"
    HighCard = 0

    for x in range(0,5):
        Numba[x] = FiveCards[x][0]                      # Numba is a list of card number values
        Numba.append("")
    del Numba[5]

    Numba.sort()
    if Numba[4] - Numba[3] == 1:
        if Numba[3] - Numba[2] == 1:
            if Numba[2] - Numba[1] == 1:
                if Numba[1] - Numba[0] == 1:
                    HandType = "Straight"
                    HighCard = Numba[4]
    return HandType, HighCard

def Compare(HandInfo1, HandInfo2):

    Winner = "Tie"
    HandTree = ["StraightFlush", "FourOfAKind", "Flush", "Straight", "Trips", "TwoPair", "OnePair", "HighCard"]


    if HandTree.index(HandInfo1[0]) < HandTree.index(HandInfo2[0]):
        Winner = "Hand1"
    elif HandTree.index(HandInfo1[0]) > HandTree.index(HandInfo2[0]):
        Winner = "Hand2"
    else:
        if HandInfo1[1] > HandInfo2[1]:
            Winner = "Hand1"
        elif HandInfo1[1] < HandInfo2[1]:
            Winner = "Hand2"
        else:
            if HandInfo1[2] > HandInfo2[2]:
                Winner = "Hand1"
            elif HandInfo1[2] < HandInfo2[2]:
                Winner = "Hand2"
    return Winner

