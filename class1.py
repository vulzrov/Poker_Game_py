import random # 只有Game类用，以后删。
# 牌型与比较

MAP = ('3','4','5','6','7','8','9','10','J','Q','K','A','2')

# 函数：bubble sort
def Bubble_Sort(cards):
    if len(cards) < 2:
        return cards
    pos = len(cards) -2
    while (cards[pos] > cards[pos+1]) and (pos > -1):
        cards[pos],cards[pos+1] = cards[pos+1], cards[pos]
        pos -= 1
    return cards

# 函数，从字符串返回牌index
def getIndex(s):
    if s == 'joker':
        return 52
    if s == 'JOKER':
        return 53
    # suit map
    SPADE = chr(9824)
    BLOSSOM = chr(9827)
    HEART = chr(9829)
    PIECE = chr(9830)
    SUIT_MAP = (SPADE,BLOSSOM,HEART,PIECE)

    # key map
    KEY_MAP = ('3','4','5','6','7','8','9','10','J','Q','K','A','2')

    for pos in range(4):
        if SUIT_MAP[pos] == s[0]:
            break
    suit = pos

    for pos in range(13):
        if KEY_MAP[pos] == s[1:]:
            break
    key = pos
    return suit * 13 + key

# 数据类型：牌
# 特别定义：空牌。用于初始化。(理解为占位符)
# 空牌 index = -1, 作为默认值。
# 空牌的suit属性为''，空字符串。
# key属性为-1。
# Show属性为'',空字符串。
class Card:
    '''有花色suit、大小key、序列号index、字符串表示Show四个属性。输入序列号构建。'''
    def __init__(self, index = -1):
        # 属性：花色
        self.suit = self.getsuit(index)        
        # 属性：大小
        self.key = self.getkey(index)
        # 属性：序列号
        self.index = index
        # 属性：字符串表示
        self.Show = self.__str__()

    # 获取面值。小王为13，大王为14。
    def getkey(self,index):
        if index == -1:
            return -1
        if index // 13 < 4:
            return index % 13
        else:
            return 13 + index % 13

    #获取花色
    def getsuit(self,index):
        if index == -1:
            return ''
        SPADE = chr(9824)
        BLOSSOM = chr(9827)
        HEART = chr(9829)
        PIECE = chr(9830)

        SUIT_MAP = (SPADE,BLOSSOM,HEART,PIECE)

        if index // 13 < 4:
            return SUIT_MAP[index // 13]
        else:
            if index % 13 == 0:
                return 'joker'
            else:
                return 'JOKER'

    # 属性：字符串显示。
    def __str__(self):
        if self.key < 0:
            return ''
        elif (self.key >= 0 and self.key <= 7):
            return '{}{}'.format(self.suit,self.key+3)
        elif self.key == 8:
            return '{}J'.format(self.suit)
        elif self.key == 9:
            return '{}Q'.format(self.suit)
        elif self.key == 10:
            return '{}K'.format(self.suit)
        elif self.key == 11:
            return '{}A'.format(self.suit)
        elif self.key == 12:
            return '{}2'.format(self.suit)
        else:
            return '{}'.format(self.suit)

    # 定义牌之间的小于、等于、大于关系。
    def __lt__(self, other):

        return self.key < other.key
    def __gt__(self, other):

        return self.key > other.key
    def __eq__(self, other):

        return self.index == other.index

# 数据类型：牌堆CardStack。是各类一个用于继承的父类。
class CardStack:

    '''数据类型：牌堆。是各类牌型的父类。
       Construtor接受一串无序整数作为参数。
       属性有：
            1. self.cards。Card list。按key属性排序，模拟人的整牌动作。
            2. self.indexs。int list。按key属性排序，模拟人的整牌动作。
            3. self.Show。str。用于可视化牌堆。
       方法有：
            1. self.Add。向牌堆添牌。可以添一个（card），可以添一堆（sequence）。可以用index表示牌，也可以用card表示牌。但注意参数不能是CardStack。
            2. self.GiveOut。从牌堆出牌。可以出一个（card），可以出一堆（sequence）。可以用index表示牌，也可以用card表示牌。但注意参数不能是CardStack。'''

    def __init__(self,indexs = [-1]): #解释：indexs为一串对应着牌的无序数字, 一个序列。
        self.cards = self.Construct_Cards(indexs)
        self.indexs = self.Construct_Indexs(self.cards)
        self.Show = self.__str__()
        # self.indexs按对应的Card.key排，而不是按index本身大小。

    # 建牌堆。
    # 牌堆是按key属性排序的，模拟人的整牌动作。
    # 算法实现为append + bubble sort(取思路，再简化)。因为似乎原思路’插入‘和这个的复杂度没区别。
    def Construct_Cards(self,indexes):
        cards = []
        for index in indexes:
            new = Card(index)
            cards.append(new)
            cards = Bubble_Sort(cards)
        return cards

    # 建牌堆对应的index堆。
    def Construct_Indexs(self,cards):
        indexs = []
        for card in cards:
            indexs.append(card.index)
        return indexs

    # 向牌堆添牌。可以添一个（card），可以添一堆（sequence）。可以用index表示牌，也可以用card表示牌。
    def Add(self,cards):
        Cards = cards
        # 第一步，标准化输入为cards sequence。
        if type(Cards) == type(Card(0)):
            Cards = [Cards]
        elif type(Cards) == type(0):
            Cards = [Card(Cards)]
        else:
            try:
                if type(Cards[0]) == type(0):
                    Cards = self.Construct_Cards(Cards)
                else:
                    pass
            except:
                print('Error occur. ilegal input format.')
                return

        # 第二步，判断输入是否合法。（要添的牌牌堆里是否已存在？）
        for new in Cards:
            if new in self.cards:
                return -1

        # 第三步，更新self.cards属性。要排除可能存在的占位符。
        if self.cards == [Card()]:
            self.cards.pop()
        for new in Cards:
            self.cards.append(new)
            self.cards = Bubble_Sort(self.cards)

        # 第四步，更新self.indexs属性。
        self.indexs = self.Construct_Indexs(self.cards)

        self.Show = self.__str__()

        return 0

    # 从牌堆出牌。可以出一个（card），可以出一堆（sequence）。可以用index表示牌，也可以用card表示牌。
    def GiveOut(self,cards):
        Cards = cards
        # 第一步，标准化输入为cards sequence。
        if type(Cards) == type(Card(0)):
            Cards = [Cards]          
        elif type(Cards) == type(0):
            Cards = [Card(Cards)]
        else:
            try:
                if type(Cards[0]) == type(0):
                    Cards = self.Construct_Cards(Cards)
                else:
                    pass
            except:
                print('Error occur. ilegal input format.')
                return

        # 第二步，判断输入是否合法。（要出的牌堆里有没有？）
        for new in Cards:
            if new not in self.cards:
                return -1

        # 第三步，更新self.cards属性。如果更新后为空，要加上占位符。
        for new in Cards:
            self.cards.remove(new)

        if len(self.cards) == 0:
            self.cards = [Card()]


        # 第四步，更新self.indexs属性。
        self.indexs = self.Construct_Indexs(self.cards)  
        
        self.Show = self.__str__()
        return 0

    def __str__(self):
        result = []
        for card in self.cards:
            result.append(card.Show)
        return ' '.join(result)

# 牌堆CardStack子类一：打出的牌
class Deck(CardStack):
    '''CardStack子类一：打出的牌。
       Construtor接受一串无序整数作为参数。
       继承的属性：
            1. self.cards。Card list。按key属性排序，模拟人的整牌动作。
            2. self.indexs。int list。按key属性排序，模拟人的整牌动作。
            3. self.Show。str。用于可视化牌堆。
       额外属性： 
            1.self.Type，打出的牌的类型；
            2.self.ComparableKey，同类型比较大小时用到的 ComparableKey 值，无效出牌为-1。
       {0 ：单走，1：对子，2：三条，3：无翼飞机，4：三带一，5：三带二，6：单翼飞机，7：双翼飞机，8：顺子，9：连对，10：炸弹，11：无效类型}'''

    def __init__(self, indexs = [-1]): #解释：indexs为一串对应着牌的无序数字, 一个序列。
        
        CardStack.__init__(self,indexs)
        self.Type = self.GetType()
        self.ComparableKey = self.GetComparableKey(self.Type)

    # 是三条
    def isThree(self, cards):
        if len(cards) == 3 and (cards[0].key == cards[1].key) and (cards[1].key == cards[2].key):
            return True
        return False

    # 获取牌堆中最长的一组连续的牌
    def getLongest(self,cards):
        '''返回对象为牌堆中最长的一组连续的牌组成的列表，非牌堆'''
        Cards = cards[:]
        result = []
        cache = []
        while (len(Cards) > 0):
            new = Cards.pop(0)
            if len(cache) == 0:
                cache.append(new)
            else:
                if new.key == cache[-1].key:
                    cache.append(new)
                else:
                    if len(cache) > len(result):
                        result = cache
                        cache = [new]
                    else:
                        cache = [new]
        if len(cache) > len(result):
            return cache
        return result

    # 是普通炸弹。
    def isBoomber(self,cards):
        if len(cards) != 4:
            return False
        if (cards[0].key == cards[1].key) and (cards[1].key == cards[2].key) and (cards[2].key == cards[3].key):
            return True
        return False

    # 是王炸。
    def isGrandBoomber(self,cards):
        if len(cards) != 2:
            return False
        if cards[0].key == 13 and cards[1].key == 14:
            return True
        return False

    # 是三带二
    def isThreeTwo(self, cards):
        if len(cards) != 5:
            return False
        if len(self.getLongest(cards)) == 3:
            return True
        return False
        
    # 是顺子
    def isFlush(self, cards):
        if len(cards) < 5:
            return False
        for pos in range(len(cards)-1):
            if cards[pos].key != (cards[pos+1].key-1):
                return False
        return True

    # 是连对
    def isChainPair(self, cards):
        if len(cards) < 6 or len(cards)%2 != 0:
            return False
        itr_even = 2
        itr_odd = 3
        while (itr_even < len(cards)) and (itr_odd < len(cards)):
            if cards[itr_even].key != cards[itr_odd].key:
                return False
            if (cards[itr_even].key != cards[itr_even-2].key+1) or (cards[itr_odd].key != cards[itr_odd-2].key+1):
                return False
            itr_even += 2
            itr_odd += 2
        return True

    # 是无翼飞机
    def isRawPlane(self, cards):
        if len(cards) != 6:
            return False
        if len(self.getLongest(cards)) != 3:
            return False
        if self.isThree(cards[:3]) and self.isThree(cards[3:]) and (cards[0].key == cards[-1].key-1):
            return True
        return False

    # 是单翼飞机
    def isMonoPlane(self,cards):
        Cards = cards.copy()
        if len(cards) != 8:
            return False
        # 机翼机身先分装到不同栈里再测试。
        body_part1 = self.getLongest(Cards)
        Cards = [card for card in Cards if card not in body_part1]
        body_part2 = self.getLongest(Cards)
        body = body_part1 + body_part2
        wings = [card for card in Cards if card not in body_part2]
        if self.isRawPlane(body):
            return True
        return False

    # 是双翼飞机
    def isBiPlane(self,cards):
        Cards = cards[:]
        if len(Cards) != 10:
            return False
        # 机翼机身先分装到不同栈里再测试。
        body_part1 = self.getLongest(Cards)
        Cards = [card for card in Cards if card not in body_part1]
        body_part2 = self.getLongest(Cards)
        Cards = [card for card in Cards if card not in body_part2]
        body = body_part1 + body_part2
        wing1 = self.getLongest(Cards)
        wing2 = self.getLongest([card for card in Cards if card not in wing1])
        if self.isRawPlane(body) and len(wing1) == 2 and len(wing2) == 2:
            return True
        return False
    
    # 获取牌型
    def GetType(self):
        '''{0 ：单走，1：对子，2：三条，3：无翼飞机，4：三带一，5：三带二，6：单翼飞机，7：双翼飞机，8：顺子，9：连对，10：炸弹，11：无效类型}'''


        # 单走
        if len(self.cards) == 1:
            # 排除占位符
            if self.cards == [Card()]:
                return -1
            else:
                return 0
        # 对子,王炸（和普通炸弹判断分开，归类相同）。
        elif len(self.cards) == 2:
            if (self.cards[0].key == self.cards[1].key):
                return 1
            elif self.isGrandBoomber(self.cards):
                return 10
            else:
                return 11
        # 三条
        elif len(self.cards) == 3:
            if self.isThree(self.cards):
                return 2
            else:
                return 11
        # 三带一，普通炸弹（和王炸判断分开，归类相同）。
        elif len(self.cards) == 4:
            # 炸弹
            if self.isBoomber(self.cards):
                return 10
            # 三带一
            elif (self.isThree(self.cards[:3]) or self.isThree(self.cards[1:])):
                return 4
            # 无效组合
            else:
                return 11
        # 三带二/顺子/无翼飞机/单翼飞机/双翼飞机/连对
        else:
            # 三带二
            if self.isThreeTwo(self.cards):
                return 5
            # 顺子
            elif self.isFlush(self.cards):
                return 8
            # 无翼飞机
            elif self.isRawPlane(self.cards):
                return 3
            # 单翼飞机
            elif self.isMonoPlane(self.cards):
                return 6
            # 双翼飞机
            elif self.isBiPlane(self.cards):
                return 7
            # 连对
            elif self.isChainPair(self.cards):
                return 9
            # 无效组合
            else:
                return 11

    # 获取比较用的ComparableKey
    def GetComparableKey(self,type):
        '''{0 ：单走，1：对子，2：三条，3：无翼飞机，4：三带一，5：三带二，6：单翼飞机，7：双翼飞机，8：顺子，9：连对，10：炸弹，11：无效类型}'''
        if type == -1:
            return -1
        elif type >= 0 and type <= 3:
            return self.cards[0].key
        elif type >= 4 and type <= 7:
            return self.getLongest(self.cards)[0].key
        elif type == 8 or type == 9:
            return (len(self.cards),self.cards[0].key)
        elif type == 10:
            return 13 + self.cards[0].key
        else:
            return -1

    # 重定义Add
    def Add(self, cards):
        Cards = cards
        # 第一步，标准化输入为cards sequence。
        if type(Cards) == type(Card(0)):
            Cards = [Cards]
        elif type(Cards) == type(0):
            Cards = [Card(Cards)]
        else:
            try:
                if type(Cards[0]) == type(0):
                    Cards = self.Construct_Cards(Cards)
                else:
                    pass
            except:
                print('Error occur. ilegal input format.')
                return

        # 第二步，判断输入是否合法。（要添的牌牌堆里是否已存在？）
        for new in Cards:
            if new in self.cards:
                return -1

        # 第三步，更新self.cards属性。要排除可能存在的占位符。
        if self.cards == [Card()]:
            self.cards.pop()
        for new in Cards:
            self.cards.append(new)
            self.cards = Bubble_Sort(self.cards)

        # 第四步，更新self.indexs属性。
        self.indexs = self.Construct_Indexs(self.cards)

        self.Show = self.__str__()
        self.Type = self.GetType()
        self.ComparableKey = self.GetComparableKey(self.Type)
        return 0
        
    # 重定义GiveOut
    def GiveOut(self, cards):
        Cards = cards
        # 第一步，标准化输入为cards sequence。
        if type(Cards) == type(Card(0)):
            Cards = [Cards]          
        elif type(Cards) == type(0):
            Cards = [Card(Cards)]
        else:
            try:
                if type(Cards[0]) == type(0):
                    Cards = self.Construct_Cards(Cards)
                else:
                    pass
            except:
                print('Error occur. ilegal input format.')
                return

        # 第二步，判断输入是否合法。（要出的牌堆里有没有？）
        for new in Cards:
            if new not in self.cards:
                return -1

        # 第三步，更新self.cards属性。如果更新后为空，要加上占位符。
        for new in Cards:
            self.cards.remove(new)

        if len(self.cards) == 0:
            self.cards = [Card()]


        # 第四步，更新self.indexs属性。
        self.indexs = self.Construct_Indexs(self.cards)  
        
        self.Show = self.__str__()
        self.Type = self.GetType()
        self.ComparableKey = self.GetComparableKey(self.Type)
        return 0
        

# 牌堆CardStack子类二：AI玩家
class AI(CardStack):
    '''牌堆CardStack子类二：AI玩家
       功能：读取缓冲区内的Deck，遍历自己的手牌整理出能压住缓冲区Deck的牌，打出。
       实现：self.Response方法。接受一个Deck对象，输出能压住缓冲区Deck的牌，返回Deck对象。如果不能回应，返回-1.'''

    def __init__(self,indexs): #解释：indexs为一串对应着牌的无序数字, 一个序列。
        CardStack.__init__(self,indexs)

    # 回应type = 0, 单牌
    def RespondToSingle(self, key):
        if len(self.cards) < 1:
            return -1
        for card in self.cards:
            # 抓取目标
            if card.key > key:
                # 抓到了，先更新self
                self.GiveOut(card)
                # 再输出
                return Deck([card.index])
        # 没有符合的项，回应-1，意为”回应不了啦“。
        return -1
    # 回应type = 1, 对子
    def RespondToPair(self,key):
        if len(self.cards) < 2:
            return -1
        Cards = self.cards[:]
        cache = []
        while(len(Cards) > 0):
            card = Cards.pop(0)
            if card.key <= key:
                continue
            if len(cache) == 0:
                cache.append(card)
            else:
                if card.key != cache[0].key:
                    cache = [card]
                else:
                    cache.append(card)
                    break
        if len(cache) == 2:
            self.GiveOut(cache)
            indexs = [card.index for card in cache]            
            return Deck(indexs)
        else:
            return -1
    # 回应type = 2，三条
    def RespondToThree(self,key):
        if len(self.cards) < 3:
            return -1
        Cards = self.cards[:]
        cache = []
        while(len(Cards) > 0):
            card = Cards.pop(0)
            if card.key <= key:
                continue
            else:
                if len(cache) == 0:
                    cache.append(card)
                elif len(cache) == 1:
                    if card.key != cache[0].key:
                        cache = [card]
                    else:
                        cache.append(card)
                else:
                    if card.key != cache[-1].key:
                        cache = [card]
                    else:
                        cache.append(card)
                        break
        if len(cache) == 3:
            self.GiveOut(cache)
            indexs = [card.index for card in cache]            
            return Deck(indexs)
        else:
            return -1
    # 回应type = 3, 无翼飞机
    def RespondToRawPlane(self,key):
        if len(self.cards) < 6:
            return -1
        for pos in range(len(self.cards)-5):
            if self.cards[pos].key <= key:
                continue
            else:
                if Deck([0]).isRawPlane(self.cards[pos:pos+6]):
                    indexs = [card.index for card in self.cards[pos:pos+6]]
                    self.GiveOut(indexs)
                    return Deck(indexs)
        return -1
    # 回应type = 4, 三带一
      # 实现：1.找三条 2.取最小的单牌 3.再判断是否组成了炸弹
    def RespondToThreeOne(self,key):
        if len(self.cards) < 4:
            return -1
        result = []
        for pos in range(len(self.cards)-2):
            if self.cards[pos].key <= key:
                continue
            else:
                if Deck([0]).isThree(self.cards[pos:pos+3]):
                    result = self.cards[pos:pos+3]
                    break
        if len(result) != 3:
            return -1
        else:
            itr = 0
            result.append(self.cards[itr])
            while (Deck([0]).isBoomber(result) and itr < len(self.cards)):
                result.pop()
                itr += 1
                result.append(self.cards[itr])
            if len(result) == 4:
                indexs = [card.index for card in result]
                self.GiveOut(indexs)
                return Deck(indexs)
            return -1
    # 回应type = 5, 三带二
    def RespondToThreeTwo(self,key):
        if len(self.cards) < 5:
            return -1
        result = []
        for pos in range(len(self.cards)-2):
            if self.cards[pos].key <= key:
                continue
            else:
                if Deck([0]).isThree(self.cards[pos:pos+3]):
                    result = self.cards[pos:pos+3]
                    break
        if len(result) != 3:
            return -1
        else:
            for card in self.cards:
                if len(result) >= 5:
                    break
                else:
                    if card.key != result[0].key and card.key != result[-1].key:
                        result.append(card)
            if len(result) == 5:
                indexs = [card.index for card in result]
                self.GiveOut(indexs)
                return Deck(indexs)
            else:
                return -1
    # 回应type = 6, 单翼飞机
    def RespondToMonoPlane(self,key):
        if len(self.cards) < 8:
            return -1
        result = []
        for pos in range(len(self.cards)-5):
            if self.cards[pos].key <= key:
                continue
            else:
                if Deck([0]).isRawPlane(self.cards[pos:pos+6]):
                    result = self.cards[pos:pos+6]
                    break
        if len(result) != 6:
            return -1
        else:
            for card in self.cards:
                if len(result) >= 8:
                    break
                else:
                    if card.key != result[0].key and card.key != result[3].key and card.key != result[-1].key and len(result) < 8:
                        result.append(card)
            if len(result) == 8:
                indexs = [card.index for card in result]
                self.GiveOut(indexs)
                return Deck(indexs)
            else:
                return -1
    # 回应type = 7，双翼飞机
    def RespondToBiPlane(self,key):
        if len(self.cards) < 10:
            return -1
        result = []
        for pos in range(len(self.cards)-5):
            if self.cards[pos].key <= key:
                continue
            else:
                if Deck([0]).isRawPlane(self.cards[pos:pos+6]):
                    result = self.cards[pos:pos+6]
                    break
        if len(result) != 6:
            return -1
        else:
            cache = []
            Cards = [card for card in self.cards if (card.key != result[0].key and card.key != result[-1].key)]
            while len(Cards) > 0:
                new = Cards.pop(0)
                if len(cache) == 0:
                    cache.append(new)
                elif len(cache) == 1:
                    if new.key != cache[0].key:
                        cache = [new]
                    else:
                        cache.append(new)
                elif len(cache) == 2:
                    if new.key == cache[-1].key:
                        continue
                    else:
                        cache.append(new)
                elif len(cache) == 3:
                    if new.key == cache[-1].key:
                        cache.append(new)
                        break
                    else:
                        cache.pop()
                        cache.append(new)
            if len(cache) != 4:
                return -1
            else:
                result = result + cache
                indexs = [card.index for card in result]
                self.GiveOut(indexs)
                return Deck(indexs)
    # 回应type = 8, 顺子
    def RespondToFlush(self,ComparableKey):
        if len(self.cards) < 5:
            return -1
        length, key = ComparableKey
        if len(self.cards) < length:
            return -1
        result = []
        Cards = [card for card in self.cards if card.key < 11]
        while (len(result) < length and len(Cards) > 0):
            new = Cards.pop(0)
            if new.key <= key:
                continue
            else:
                if len(result) == 0:
                    result.append(new)
                else:
                    if new.key == (result[-1].key + 1):
                        result.append(new)
                    elif new.key == result[-1].key:
                        continue
                    else:
                        result = [new]

        if len(result) == length:
            indexs = [card.index for card in result]
            self.GiveOut(indexs)
            return Deck(indexs)
        else:
            return -1
    # 回应type = 9, 连对
    def RespondToChainPair(self,ComparableKey):
        if len(self.cards) < 6:
            return -1
        length, key = ComparableKey
        if len(self.cards) < length:
            return -1
        result = []
        Cards = [card for card in self.cards if card.key < 11]
        while (len(result) < length and len(Cards) > 0):
            new = Cards.pop(0)
            if new.key <= key:
                continue
            if len(result) == 0:
                result.append(new)
            else:
                # result长度为奇数，检查new与result[-1]的key是否相等
                if len(result)%2 == 1:
                    if new.key == result[-1].key:
                        result.append(new)
                    else:
                        result = [new]
                # result长度为偶数，检查new与result[-1]的key是否连续
                else:
                    if new.key == result[-1].key+1:
                        result.append(new)
                    elif new.key == result[-1].key:
                        continue
                    else:
                        result = [new]
        if len(result) == length:
            indexs = [card.index for card in result]
            self.GiveOut(indexs)
            return Deck(indexs)
        else:
            return -1
    # 回应type = 10, 炸弹
    # 首先是普通的炸弹。                    
    def RespondToBoomber(self,key):
        if len(self.cards) < 4:
            return -1
        Cards = self.cards
        cache = []
        while(len(Cards) > 0):
            card = Cards.pop(0)
            if card.key <= key:
                continue
            else:
                if len(cache) == 0:
                    cache.append(card)
                elif len(cache) == 1 or len(cache) == 2:
                    if card.key != cache[-1].key:
                        cache = [card]
                    else:
                        cache.append(card)
                else:
                    if card.key != cache[-1].key:
                        cache = [card]
                    else:
                        cache.append(card)
                        break
        if len(cache) == 4:
            self.GiveOut(cache)
            indexs = [card.index for card in cache]            
            return Deck(indexs)
        else:
            return -1
    # 王炸不可能回应。只能回-1。

    # 找个炸弹。
    # 首先是普通的
    def findBoomer(self):
        if len(self.cards) < 4:
            return -1
        Cards = self.cards[:]
        cache = []
        while(len(Cards) > 0):
            new = Cards.pop(0)
            if len(cache) == 0:
                cache.append(new)
            elif len(cache) == 1 or len(cache) == 2:
                if new.key == cache[-1].key:
                    cache.append(new)
                else:
                    cache = [new]
            else:
                if new.key == cache[-1].key:
                    cache.append(new)
                    break
                else:
                    cache = [new]
        if len(cache) == 4:
            indexs = [card.index for card in cache]
            self.GiveOut(indexs)
            return Deck(indexs)
        else:
            return -1
    # 然后是王炸
    def findGrandBoomber(self):
        if len(self.cards) < 2:
            return -1
        if self.cards[-2].key != 13:
            return -1
        if self.cards[-1].key != 14:
            return -1
        Cards = self.cards[-2:]
        indexs = [card.index for card in Cards]
        self.GiveOut(indexs)
        return Deck(indexs)

    # 判断是不是出完了。出完就赢了。
    def isEmpty(self):
        if self.indexs == [-1]:
            return True
        return False

    def Response(self,deck):
        ''' 根据Type使用不同算法进行遍历整理。
        回应（返回值）应该是Deck对象。如果无法返回，回应-1。
        先看能不能正常回应，再找炸弹，再找王炸。都不行就返回-1。'''
        type = deck.Type
        key = deck.ComparableKey

        # 回应空。
        if type == -1:
            response = self.cards[0]
            indexs = [response.index]
            self.GiveOut(indexs)
            return Deck(indexs)
        # 回应type = 0, 单牌
        elif type == 0:
            response = self.RespondToSingle(key)
            if response != -1:
                return response
            else:
                response = self.findBoomer() 
                if response != -1:
                    return response
                else:
                    return self.findGrandBoomber()
        # 回应type = 1, 对子
        elif type == 1:
            response = self.RespondToPair(key)
            if response != -1:
                return response
            else:
                response = self.findBoomer() 
                if response != -1:
                    return response
                else:
                    return self.findGrandBoomber()
        # 回应type = 2，三条
        elif type == 2:
            response = self.RespondToThree(key)
            if response != -1:
                return response
            else:
                response = self.findBoomer() 
                if response != -1:
                    return response
                else:
                    return self.findGrandBoomber()
        # 回应type = 3, 无翼飞机
        elif type == 3:
            response = self.RespondToRawPlane(key)
            if response != -1:
                return response
            else:
                response = self.findBoomer() 
                if response != -1:
                    return response
                else:
                    return self.findGrandBoomber()
        # 回应type = 4, 三带一
        elif type == 4:
            response = self.RespondToThreeOne(key)
            if response != -1:
                return response
            else:
                response = self.findBoomer() 
                if response != -1:
                    return response
                else:
                    return self.findGrandBoomber()
        # 回应type = 5, 三带二
        elif type == 5:
            response = self.RespondToThreeTwo(key)
            if response != -1:
                return response
            else:
                response = self.findBoomer() 
                if response != -1:
                    return response
                else:
                    return self.findGrandBoomber()
        # 回应type = 6, 单翼飞机
        elif type == 6:
            response = self.RespondToMonoPlane(key)
            if response != -1:
                return response
            else:
                response = self.findBoomer() 
                if response != -1:
                    return response
                else:
                    return self.findGrandBoomber()
        # 回应type = 7, 双翼飞机
        elif type == 7:
            response = self.RespondToBiPlane(key)
            if response != -1:
                return response
            else:
                response = self.findBoomer() 
                if response != -1:
                    return response
                else:
                    return self.findGrandBoomber()
        # 回应type = 8, 顺子
        elif type == 8:
            response = self.RespondToFlush(key)
            if response != -1:
                return response
            else:
                response = self.findBoomer() 
                if response != -1:
                    return response
                else:
                    return self.findGrandBoomber()
        # 回应type = 9, 连对
        elif type == 9:
            response = self.RespondToChainPair(key)
            if response != -1:
                return response
            else:
                response = self.findBoomer() 
                if response != -1:
                    return response
                else:
                    return self.findGrandBoomber()
        # 回应type = 10, 炸弹
        elif type == 10:

            return self.RespondToBoomber(key)
        # 无效类型 type = 11
        else:

            return -1

    def __call__(self,deck):

        return self.Response(deck)

# 对象：游戏
class Game:
    '''游戏对象'''

    def __init__(self):
        # 第一步，生成initializers。
        stack = list(range(54))
        initializers = [[],[],[]]
        for initializer in initializers:
            for _ in range(18):
                digit = stack[random.randint(0,len(stack)-1)]
                stack.remove(digit)
                initializer.append(digit)

        # 第二步，生成三个牌堆。
        self.AI1 = AI(initializers[0])
        self.AI2 = AI(initializers[1])
        self.Human = CardStack(initializers[2])



    def __str__(self):
        result = []
        result.append(self.AI1.Show)
        result.append(self.AI2.Show)
        result.append(self.Human.Show)
        return '\n'.join(result)

        
        



    
    
