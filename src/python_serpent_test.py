from ethereum import tester as t
import math
import os

initial_gas = 0

def test_cash():
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('data_api/cash.se')
    
    c.initiateOwner(111)
    c.setCash(111, 10)
    gas_use(s)
    c.addCash(111,5)
    c.subtractCash(111,4)
    gas_use(s)
    assert(c.balance(111)==11), "Cash value not expected!"
    gas_use(s)
    c.send(111, 10)
    assert(c.send(47, 10)==0), "Receiver check broken"
    assert(c.balance(111)==21), "Send function broken"
    assert(c.sendFrom(101, 1, 111)==0), "Receiver uninitialized check failed"
    c.initiateOwner(101)
    assert(c.sendFrom(101, 1, 111)==1), "Send from broken"
    assert(c.balance(111)==20), "Send from broken"
    assert(c.balance(101)==1), "Send from broken"
    assert(c.setCash(447, 101)==0), "Set cash owner check broken"
    gas_use(s)
    print "CASH OK"
    
def test_ether():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('data_api/ether.se')
    assert(c.depositEther(value=5)==5), "Unsuccessful eth deposit"
    assert(c.withdrawEther(111, 500)==0), "Printed money out of thin air..."
    assert(c.withdrawEther(111, 5)==1), "Unsuccessful withdrawal"
    gas_use(s)
    print "ETHER OK"
    
def test_exp():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('data_api/expiringEvents.se')
    c.setReportHash(1010101, 0, 101, 47, 0)
    assert(c.getReportHash(1010101, 0, 101, 0)==47), "Report hash wrong"
    c.addEvent(1010101, 0, 447)
    assert(c.getEvent(1010101, 0, 0) == 447), "Add/get event broken"
    assert(c.getNumberEvents(1010101, 0)==1), "Num events wrong"
    assert(c.setNumEventsToReportOn(1010101, 0)==-1), "Vote period check issue"
    c.moveEventsToCurrentPeriod(1010101, 1, 2)
    assert(c.getEvent(1010101, 2, 0) == 447), "Move events broken"
    assert(c.sqrt(25*2**64)==5*2**64), "Square root broken"
    print "EXPIRING EVENTS OK"
    gas_use(s)

def test_quicksort():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('functions/quicksort.se')
    array = [1, 40, 2, 30, 44, 33, 22, 12, 22, 43]
    assert(c.quicksort(array) == [1, 2, 12, 22, 22, 30, 33, 40, 43, 44]), "Quicksort broken"
    print "QUICKSORT OK"
    gas_use(s)

def test_insertionsort():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('functions/insertionsort.se')
    array = [1, 40, 2, 30, 44, 33, 22, 12, 22, 43]
    assert(c.insertionSort(array) == [1, 2, 12, 22, 22, 30, 33, 40, 43, 44]), "Insertion sort broken"
    print "INSERTIONSORT OK"
    gas_use(s)
    
def test_log_exp():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('data_api/fxpFunctions.se')
    assert(c.fx_exp(2**64) == 50143449209799256664), "Exp broken"
    assert(c.fx_log(2**64) == 7685), "Log broken"
    print "LOG EXP OK"
    xs = [2**64, 2**80, 2**68, 2**70]
    maximum = max(xs)
    sum = 0
    original_method_sum = 0
    i = 0
    while i < len(xs):
        sum += c.fx_exp(xs[i] - maximum)
        original_method_sum += c.fx_exp(xs[i])
        i += 1
    print maximum + c.fx_log(sum)
    print c.fx_log(original_method_sum)
    gas_use(s)

def test_markets():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('data_api/markets.se')
    gas_use(s)
    c.initializeMarket(444, [445, 446, 447], 1, 2**57, 1010101, 2)
    c.initialLiquiditySetup(444, 2**55, 1, 2)
    c.setWinningOutcomes(444, [2])
    assert(c.getWinningOutcomes(444)[0] == 2), "Winning outcomes wrong"
    assert(c.addParticipant(444, s.block.coinbase)==0), "Participant adding issue"
    #modifyShares(market, outcome, amount)
    #modifyParticipantShares(branch, marketID, participantNumber, outcome, amount)
    #lsLmsr(marketID)
    #c.getParticipantSharesPurchased(market, participantNumber, outcome)
    # getMarketEvent singular
    assert(c.getParticipantNumber(444, s.block.coinbase)==0), "Participant number issue"
    assert(c.getParticipantID(444, 0)==745948140856946866108753121277737810491401257713), "Participant ID issue"
    assert(c.getMarketEvents(444) == [445,446,447]), "Market events load/save broken"
    print "MARKETS OK"

def test_reporting():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('data_api/reporting.se')
    gas_use(s)
    assert(c.getRepByIndex(1010101, 0) == 47*2**64), "Get rep broken"
    assert(c.getReporterID(1010101, 1)==1010101), "Get reporter ID broken"
    #c.getReputation(address)
    assert(c.repIDToIndex(1010101, 1010101)==1), "Rep ID to index wrong"
    #c.claimInitialRep(parent, newBranch)
    c.addReporter(1010101, 777)
    c.addRep(1010101, 2, 55*2**64)
    c.subtractRep(1010101, 2, 2**64)
    assert(c.getRepByIndex(1010101, 2) == 54*2**64), "Get rep broken upon adding new reporter"
    assert(c.getReporterID(1010101, 2)==777), "Get reporter ID broken upon adding new reporter"
    assert(c.repIDToIndex(1010101, 777)==2), "Rep ID to index wrong upon adding new reporter"
    c.setRep(1010101, 2, 5*2**64)
    assert(c.getRepBalance(1010101, 777) == 5*2**64), "Get rep broken upon set rep"
    c.addDormantRep(1010101, 2, 5)
    c.subtractDormantRep(1010101, 2, 2)
    assert(c.getDormantRepBalance(1010101, 777)==3), "Dormant rep balance broken"
    assert(c.getDormantRepByIndex(1010101, 2)==3), "Dormant rep by index broken"
    gas_use(s)
    c.setSaleDistribution([4,44,444,4444,44444], [0, 1, 2, 3, 4], 1010101)
    assert(c.getRepBalance(1010101, 4444)==3), "Rep Balance fetch broken w/ initial distrib."
    assert(c.getReporterID(1010101, 6)==4444), "Sale distrib. reporter ID wrong"
    print "REPORTING OK"

def test_create_event():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('functions/output.se')
    gas_use(s)
    c.initiateOwner(1010101)
    assert(c.createEvent(1010101, "new event", 555, 1, 2, 2, 0)>2**64), "binary Event creation broken"
    assert(c.createEvent(1010101, "new event", 555, 1, 5, 5, 0)>2**64), "categorical Event creation broken"
    assert(c.createEvent(1010101, "new event", 555, 1, 200, 2, 0)<-2**64), "scalar Event creation broken"
    gas_use(s)
    print "EVENT CREATION OK"

def test_create_market():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('functions/output.se')
    gas_use(s)
    c.initiateOwner(1010101)
    # binary
    event1 = c.createEvent(1010101, "new event", 555, 1, 2, 2, 0)
    # scalar
    event2 = c.createEvent(1010101, "new event", 555, 1, 200, 2, 0)
    # categorical
    event3 = c.createEvent(1010101, "new event", 555, 1, 5, 5, 0)
    # scalar
    event4 = c.createEvent(1010101, "new event", 555, -100, 200, 2, 0)
    # binary
    event5 = c.createEvent(1010101, "new event", 557, 1, 2, 2, 0)
    # scalar
    event6 = c.createEvent(1010101, "new event", 557, 1, 25, 2, 0)

    gas_use(s)
    
    ### Single Markets
    # binary market
    gas_use(s)
    bin_market = c.createMarket(1010101, "new market", 2**58, 100*2**64, 184467440737095516, [event1], 0, 1)
    print bin_market
    gas_use(s)
    print c.getSharesPurchased(bin_market, 1)
    print c.getSharesPurchased(bin_market, 2)
    # scalar market
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event2], 0, 1) 
    # odd range scalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event4], 0, 1)
    # categorical market
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event3], 0, 1)
    print "1D Done"
    
    ### 2D Markets
    # scalar + scalar market
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event2, event4], 0, 1)
    # nonscalar, scalar
    x = c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event1, event2], 0, 1)
    assert(c.getMarketNumOutcomes(x)==4), "Market num outcomes wrong"

    # scalar, nonscalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event4, event1], 0, 1)
    # nonscalar, nonscalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event5, event1], 0, 1)
    print "2D Done"
    
    ### 3D Markets
    # scalar, scalar, scalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event5, event2, event6], 0, 1)
    # scalar, nonscalar, scalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event2, event3, event4], 0, 1)
    # nonscalar, scalar, scalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event1, event2, event4], 0, 1)
    # nonscalar, nonscalar, scalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event5, event3, event6], 0, 1)
    # scalar, scalar, nonscalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event2, event4, event5], 0, 1)
    # scalar, nonscalar, nonscalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event2, event1, event3], 0, 1)
    # nonscalar, scalar, nonscalar
    market = c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event3, event2, event5], 0, 1)
    assert(c.getMarketNumOutcomes(market)==20), "Market num outcomes wrong"
    gas_use(s)
    # nonscalar, nonscalar, nonscalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event1, event5, event3], 0, 1)
    print "3D Done"
    gas_use(s)
    assert(c.getNumMarkets(event2)==9), "Num markets for event wrong"
    assert(c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event1, event5, event3], 0, 1)==-4), "Duplicate market check broken"
    assert(c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event3, event3, event3], 0, 1)==-6), "Duplicate event check broken"
    print "Market Creation OK"

def test_buy_sell_shares():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('functions/output.se')
    gas_use(s)
    c.initiateOwner(1010101)
    # binary
    event1 = c.createEvent(1010101, "new event", 555, 1, 2, 2, 0)
    # scalar
    event2 = c.createEvent(1010101, "new event", 555, 1, 200, 2, 0)
    # categorical
    event3 = c.createEvent(1010101, "new event", 555, 1, 5, 5, 0)
    # scalar
    event4 = c.createEvent(1010101, "new event", 555, -100, 200, 2, 0)
    # binary
    event5 = c.createEvent(1010101, "new event", 557, 1, 2, 2, 0)
    # scalar
    event6 = c.createEvent(1010101, "new event", 557, 1, 25, 2, 0)

    gas_use(s)
    
    ### Single Markets
    # binary market
    bin_market = c.createMarket(1010101, "new market", 2**58, 100*2**64, 184467440737095516, [event1], 0, 1)
    print c.getSharesPurchased(bin_market, 1)
    print c.getSharesPurchased(bin_market, 2)
    c.commitTrade(bin_market, c.makeMarketHash(bin_market, 2, 5*2**64, 0))
    s.mine(1)
    assert(c.buyShares(1010101, bin_market, 2, 5*2**64, 0)==1), "Buy shares issue"
    c.commitTrade(bin_market, c.makeMarketHash(bin_market, 2, 5*2**64, 0))
    s.mine(1)
    assert(c.sellShares(1010101, bin_market, 2, 5*2**64, 0)==1), "Sell shares issue"
    
    # scalar market
    a = c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event2], 0, 1)
    bal = c.balance(s.block.coinbase)
    c.commitTrade(a, c.makeMarketHash(a, 1, 15*2**64, 0))
    s.mine(1)
    # should cost ~200/share
    c.buyShares(1010101, a, 1, 15*2**64,0)
    bal_after = c.balance(s.block.coinbase)
    assert((bal-bal_after) <= 3015*2**64 and (bal-bal_after) >= 2980*2**64), "Scalar buy off"
    c.commitTrade(a, c.makeMarketHash(a, 2, 12*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.buyShares(1010101, a, 2, 12*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < 20*2**64), "Scalar buy off"
    c.commitTrade(a, c.makeMarketHash(a, 1, 15*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    print c.sellShares(1010101, a, 1, 15*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after <= -590*2**64), "Scalar sell off"
    assert(c.price(a, 1) < 2**64), "Scalar sell off"
    assert(c.price(a, 2) > 198*2**64), "Scalar sell off"

    
    # odd range scalar
    b = c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event4], 0, 1)
    bal = c.balance(s.block.coinbase)
    c.commitTrade(b, c.makeMarketHash(b, 1, 15*2**64, 0))
    s.mine(1)
    c.buyShares(1010101, b, 1, 15*2**64, 0)
    bal_after = c.balance(s.block.coinbase)
    print bal - bal_after
    assert((bal-bal_after) <= 4550*2**64 and (bal-bal_after) >= 4500*2**64), "Scalar buy off"
    c.commitTrade(b, c.makeMarketHash(b, 2, 12*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.buyShares(1010101, b, 2, 12*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < 20*2**64), "Scalar buy off"
    c.commitTrade(b, c.makeMarketHash(b, 1, 15*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.sellShares(1010101, b, 1, 15*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after <= -890*2**64), "Scalar sell off"
    assert(c.price(b, 2) > 298*2**64), "Scalar sell off"
    assert(c.price(b, 1) < 2**64), "Scalar sell off"
    c.commitTrade(b, c.makeMarketHash(b, 1, 10*2**64, 0))
    s.mine(1)
    assert(c.buyShares(1010101, b, 1, 10*2**64, 0)==1), "Buy back not working"

    # categorical market
    d = c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event3], 0, 1)
    bal = c.balance(s.block.coinbase)
    c.commitTrade(d, c.makeMarketHash(d, 1, 15*2**64, 0))
    s.mine(1)
    assert(c.price(d, 5)==c.price(d, 4)==c.price(d, 3)==c.price(d, 2)==c.price(d, 1)), "Pricing off for categorical"
    c.buyShares(1010101, d, 1, 15*2**64,0)
    bal_after = c.balance(s.block.coinbase)
    print c.price(d, 1)
    print c.price(d, 2)
    print c.price(d, 3)
    print c.price(d, 4)
    print c.price(d, 5)
    # .44 cost on avg
    # resume here
    print bal-bal_after
    assert((bal-bal_after) <= .47*15*2**64 and (bal-bal_after) >= .44*15*2**64), "Categorical buy off"
    assert(c.price(d, 1) > .68*2**64 and c.price(d, 1) < .69*2**64), "Categorical buy off"
    c.commitTrade(d, c.makeMarketHash(d, 3, 12*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.buyShares(1010101, d, 3, 12*2**64, 0)
    assert(c.price(d, 2) == c.price(d, 4) == c.price(d, 5)), "Categorical prices off"
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < .22*12*2**64 and bal-bal_after >.20*12*2**64), "Categorical buy off"
    # Sell
    c.commitTrade(d, c.makeMarketHash(d, 1, 15*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.sellShares(1010101, d, 1, 15*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    print bal-bal_after
    # 28 cents on avg / share
    assert(bal-bal_after < -4*2**64 and bal-bal_after > -5*2**64), "Categorical sell off"
    assert(c.price(d, 1) > .12*2**64 and c.price(d, 1) < .14*2**64), "Categorical sell off"
    print "1D Done"
    
    ### 2D Markets
    # scalar + scalar market
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event2, event4], 0, 1)
    # nonscalar, scalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event1, event2], 0, 1)
    # scalar, nonscalar
    e = c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event4, event1], 0, 1)
    bal = c.balance(s.block.coinbase)
    c.commitTrade(e, c.makeMarketHash(e, 1, 15*2**64, 0))
    s.mine(1)
    assert(c.getCumScale(e)==300), "Cumulative scale wrong"
    assert(c.price(e, 1) == c.price(e, 2) == c.price(e, 4) == c.price(e, 3)), "Scalar prices off"
    c.buyShares(1010101, e, 1, 15*2**64,0)
    bal_after = c.balance(s.block.coinbase)
    assert((bal-bal_after) <= 4550*2**64 and (bal-bal_after) >= 4500*2**64), "Scalar buy off"
    c.commitTrade(e, c.makeMarketHash(e, 3, 14*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.buyShares(1010101, e, 3, 14*2**64, 0)
    gas_use(s)
    print c.price(e, 1)
    print c.price(e, 2)
    print c.price(e, 3)
    print c.price(e, 4)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < 20*2**64), "Scalar buy off"
    c.commitTrade(e, c.makeMarketHash(e, 1, 15*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.sellShares(1010101, e, 1, 15*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < -300*2**64 and bal-bal_after > -320*2**64), "Scalar sell off"
    # nonscalar, nonscalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event5, event1], 0, 1)
    print "2D Done"
    
    ### 3D Markets
    # scalar, scalar, scalar
    f = c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event4, event2, event6], 0, 1)
    bal = c.balance(s.block.coinbase)
    assert(c.getCumScale(f) == 523), "3d cumscale wrong"
    c.commitTrade(f, c.makeMarketHash(f, 8, 2*2**64, 0))
    s.mine(1)
    c.buyShares(1010101, f, 8, 2*2**64,0)
    bal_after = c.balance(s.block.coinbase)
    print bal - bal_after
    assert(c.price(f,1)==c.price(f,2)==c.price(f,3)==c.price(f,4)==c.price(f,5)==c.price(f,6)==c.price(f,7)), "3d pricing broken"
    assert(c.price(f,8)>=522*2**64 and c.price(f,8) <= 524*2**64), "3d pricing broken"
    assert((bal-bal_after) <= 1055*2**64 and (bal-bal_after) >= 1005*2**64), "3d buy off"
    c.commitTrade(f, c.makeMarketHash(f, 2, 1*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.buyShares(1010101, f, 2, 1*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < 20*2**64), "3d buy off"
    c.commitTrade(f, c.makeMarketHash(f, 8, 1*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.sellShares(1010101, f, 8, 1*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < 20*2**64), "3d sell off"
    # scalar, nonscalar, scalar
    h = c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event2, event3, event4], 0, 1)
    bal = c.balance(s.block.coinbase)
    assert(c.getMarketNumOutcomes(h) == 20), "3d number outcomes wrong"
    c.commitTrade(h, c.makeMarketHash(h, 15, 15*2**64, 0))
    s.mine(1)
    assert(c.getCumScale(h) == 499), "3d cumscale wrong"
    c.buyShares(1010101, h, 15, 15*2**64,0)
    bal_after = c.balance(s.block.coinbase)
    print bal - bal_after
    assert((bal-bal_after) <= 7600*2**64 and (bal-bal_after) >= 7500*2**64), "3d buy off"
    c.commitTrade(h, c.makeMarketHash(h, 2, 12*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.buyShares(1010101, h, 2, 12*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < 20*2**64), "3d buy off"
    c.commitTrade(h, c.makeMarketHash(h, 15, 12*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.sellShares(1010101, h, 15, 12*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < 20*2**64), "3d sell off"
    # nonscalar, scalar, scalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event1, event2, event4], 0, 1)
    # nonscalar, nonscalar, scalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event5, event3, event6], 0, 1)
    # scalar, scalar, nonscalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event2, event4, event5], 0, 1)
    # scalar, nonscalar, nonscalar
    c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event2, event1, event3], 0, 1)
    # nonscalar, scalar, nonscalar
    g = market = c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event3, event2, event5], 0, 1)
    bal = c.balance(s.block.coinbase)
    assert(c.getMarketNumOutcomes(g) == 20), "3d number outcomes wrong"
    c.commitTrade(g, c.makeMarketHash(g, 8, 15*2**64, 0))
    s.mine(1)
    assert(c.getCumScale(g) == 199), "3d cumscale wrong"
    c.buyShares(1010101, g, 8, 15*2**64,0)
    bal_after = c.balance(s.block.coinbase)
    print bal - bal_after
    assert((bal-bal_after) <= 3010*2**64 and (bal-bal_after) >= 2960*2**64), "3d buy off"
    c.commitTrade(g, c.makeMarketHash(g, 2, 12*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.buyShares(1010101, g, 2, 12*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < 20*2**64), "3d buy off"
    c.commitTrade(g, c.makeMarketHash(g, 2, 12*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.sellShares(1010101, g, 2, 12*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < 20*2**64), "3d sell off"
    # nonscalar, nonscalar, nonscalar
    i = c.createMarket(1010101, "new market 2", 2**58, 100*2**64, 368934881474191032, [event1, event5, event3], 0, 1)
    bal = c.balance(s.block.coinbase)
    assert(c.getMarketNumOutcomes(i) == 20), "3d number outcomes wrong"
    c.commitTrade(i, c.makeMarketHash(i, 20, 15*2**64, 0))
    s.mine(1)
    assert(c.getCumScale(i) == 1), "3d cumscale wrong"
    c.buyShares(1010101, i, 20, 15*2**64,0)
    bal_after = c.balance(s.block.coinbase)
    print bal - bal_after
    assert((bal-bal_after) <= .13*15*2**64 and (bal-bal_after) >= .12*15*2**64), "3d buy off"
    c.commitTrade(i, c.makeMarketHash(i, 2, 12*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.buyShares(1010101, i, 2, 12*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < .12*12*2**64), "3d buy off"
    c.commitTrade(i, c.makeMarketHash(i, 20, 11*2**64, 0))
    s.mine(1)
    bal = c.balance(s.block.coinbase)
    gas_use(s)
    c.sellShares(1010101, i, 20, 11*2**64, 0)
    gas_use(s)
    bal_after = c.balance(s.block.coinbase)
    assert(bal-bal_after < -1.2*2**64 and bal-bal_after > -1.5*2**64), "3d sell off"
    print "3D Done"
    print "BUY AND SELL OK"

def test_transfer_shares():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('functions/output.se')
    gas_use(s)
    c.initiateOwner(1010101)
    # binary
    event1 = c.createEvent(1010101, "new event", 555, 1, 2, 2, 0)

    ### Single Markets
    # binary market
    bin_market = c.createMarket(1010101, "new market", 2**58, 100*2**64, 184467440737095516, [event1], 0, 1)
    c.commitTrade(bin_market, c.makeMarketHash(bin_market, 1, 15*2**64, 0))
    s.mine(1)
    c.buyShares(1010101, bin_market, 1, 15*2**64,0)
    # -1: invalid outcome or you haven't traded in this market (or market doesn't exist)
    assert(c.transferShares(1010101, bin_market, 1, 15*2**64, 444)==15*2**64), "Transfer shares fail"
    assert(c.transferShares(1010101, bin_market, 1, 15*2**64, 444)==-2), "Check for not having shares fail"
    assert(c.transferShares(1010101, 222, 1, 15*2**64, 444)==-1), "Check for invalid market fail"
    print "Transfer shares OK"

def test_create_branch():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('functions/output.se')
    gas_use(s)
    c.initiateOwner(1010101)
    b = c.createSubbranch("new branch", 100, 1010101, 2**55, 0)
    assert(b<-3 or b>3), "Branch creation fail"
    assert(c.createSubbranch("new branch", 100, 1010101, 2**55, 0)==-2), "Branch already exist fail"
    assert(c.createSubbranch("new branch", 100, 10101, 2**55, 0)==-1), "Branch doesn't exist check fail"
    assert(c.getParentPeriod(b)==c.getVotePeriod(1010101)), "Parent period saving broken"
    print "Test branch OK"

def test_send_rep():
    global initial_gas
    initial_gas = 0
    t.gas_limit = 100000000
    s = t.state()
    c = s.abi_contract('functions/output.se')
    gas_use(s)
    c.initiateOwner(1010101)
    c.reputationFaucet(1010101)
    assert(c.sendReputation(1010101, s.block.coinbase, 444)==444), "Send rep failure"
    assert(c.convertToDormantRep(1010101, 500*2**64)==0), "Allowed converting a bunch of rep to dormant that user didn't have"
    assert(c.convertToDormantRep(1010101, 444)==444), "Dormant rep conversion unsuccessful"
    assert(c.convertToActiveRep(1010101, 500*2**64)==0), "Allowed converting a bunch of rep to active that user didn't have"
    assert(c.convertToActiveRep(1010101, 444)==444), "Active rep conversion unsuccessful"
    print "Test send rep OK"

def gas_use(s):
    global initial_gas
    print "Gas Used:"
    print s.block.gas_used - initial_gas
    initial_gas = s.block.gas_used


if __name__ == '__main__':
    #os.system('python mk_test_file.py \'/home/ubuntu/workspace/src/functions\' \'/home/ubuntu/workspace/src/data_api\' \'/home/ubuntu/workspace/src/functions\'')
    # data/api tests
    #test_cash()
    #test_ether()
    #test_quicksort()
    #test_insertionsort()
    #test_log_exp()
    #test_exp()
    #test_markets()
    #test_reporting()
    
    # function tests
    #test_create_event()
    #test_create_market()
    #test_buy_sell_shares()
    #test_transfer_shares()
    #test_create_branch()
    test_send_rep()

    #close_market_tests()
    #make_report_tests()
    #consensus_tests()

    #p2p_wager_tests()
    print "DONE TESTING"