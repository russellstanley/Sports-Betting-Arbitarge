from selenium import webdriver

#Determines the potential profit from and arb
def arbitrage(odds):
    
    total = 100
    d = 0
    
    for i in odds:
        d = d + float(odds[0])/float(i)
    
    wager = total/d
    win = wager*float(odds[0])
    
    return ((win-total)/total)*100
    
#Print the results of the arb
def printResults(odds, game, date):

    print("-----------------")
    print(game)
    print(date)

    for i in enumerate(odds):
    
        total = 100
        d = 0
        
        for j in odds:
            d = d + float(odds[i[0]])/float(j)
            
        wager = round(total/d, 2)
        print("Wager " + str(i[0]+1) + ": " + str(wager))

    print("Profit(%): " + str(round(arbitrage(odds), 2)))
    print("-----------------")

#Setup browser
browser = webdriver.Chrome(executable_path='/chromedriver')

competitionid = [["NBA", 37], ["Tennis - Mens", 40], ["Tennis - Ladies", 41], ["Premier League", 1], ["English Championship", 2], ["AFL", 11], ["English League One", 62], ["National League", 99], ["German Bundesliga", 18],["Scottish Premier League", 8], ["Horse Racing", 28], ["NFL", 15], ["T20 Big Bash League", 1794]]

for i in competitionid:

    print("Analyzing " + i[0] + "...")
    URL = 'http://odds.aussportsbetting.com/betting?competitionid=' + str(i[1])
    browser.get(URL)

    #Removes sports with no game or unrecognized formats
    if browser.find_elements_by_class_name("noodds2") != []:
        print("Warning: No Games Found")
        continue
    elif browser.find_elements_by_xpath('//*[@id="tabContentTab1"]/form/table[2]') == []:
        print("Warning: Format Not Configured")
        continue
    
    #Get lines of table
    element = browser.find_element_by_xpath('//*[@id="tabContentTab1"]/form/table[2]')
    rawText = element.text
    lines = list(rawText.split("\n"))

    table = []
    found = 0
    counter = 2

    #Iterate through rows extracting the best odds
    for i in enumerate(lines):

        odds = browser.find_element_by_xpath('//*[@id="tabContentTab1"]/form/table[2]/tbody/tr[' + str(counter) + ']/td[4]')
        game = browser.find_element_by_xpath('//*[@id="tabContentTab1"]/form/table[2]/tbody/tr[' + str(counter) + ']/td[3]')
        date = browser.find_element_by_xpath('//*[@id="tabContentTab1"]/form/table[2]/tbody/tr[' + str(counter) + ']/td[2]')

        #Critera to remove table header
        if i[0]<2:
            continue
        #Remove blank odds
        elif odds.text == '- l -':
            counter = counter + 3
            continue

        oddsText = odds.text
        oddsText = list(oddsText.split(' l '))
        table.append(oddsText)
        counter = counter + 3
            
        if arbitrage(oddsText)>0:
            printResults(oddsText, game.text, date.text)
    
browser.quit()
