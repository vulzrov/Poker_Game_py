import wx
import random
import class1
import os

class MainFrame(wx.Frame):
    def __init__(self, parent, title = '阉割版欢乐斗地主',size = (200,200)):
        wx.Frame.__init__(self, parent, title = title, size = size)
        self.CreateStatusBar()

        # 菜单栏
        menu = wx.Menu()
        About = wx.MenuItem(menu, -1, '说明\tCtrl+A')
        menu.Append(About)
        self.Bind(wx.EVT_MENU,self.OnAbout,About)
        Start = wx.MenuItem(menu, -1, '开始\tCtrl+S')
        menu.Append(Start)
        self.Bind(wx.EVT_MENU,self.OnStart,Start)
        Exit = wx.MenuItem(menu, -1, '退出\tCtrl+Q')
        menu.Append(Exit)
        self.Bind(wx.EVT_MENU,self.OnExit,Exit)

        menubar = wx.MenuBar()
        menubar.Append(menu,'菜单')
        self.SetMenuBar(menubar)

        # 布局
        panel = wx.Panel(self)
        box = wx.BoxSizer()
        button = wx.Button(panel,-1,'点击开始')
        self.Bind(wx.EVT_BUTTON,self.OnStart,button)
        box.Add(button,proportion = 0, flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, border = 40)
        panel.SetSizer(box)

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, '没有叫地主抢地主功能，所以是阉割版，但欢乐不阉割哦~','小贴士')
        dlg.ShowModal()
        dlg.Destroy()

    def OnStart(self, event):
        game_window = GameFrame(self)
        game_window.Show()

    def OnExit(self, event):

        self.Close(True)

class GameFrame(wx.Frame):
    def __init__(self, parent, title = '阉割版欢乐斗地主',size = (1000,700)):
        wx.Frame.__init__(self, parent, title = title, size = size)

        # 冰山海面下
          # 第一步，生成initializers。
        stack = list(range(54))
        initializers = [[],[],[]]
        for initializer in initializers:
            for _ in range(18):
                digit = stack[random.randint(0,len(stack)-1)]
                stack.remove(digit)
                initializer.append(digit)

          # 第二步，生成三个牌堆。
        self.AI1 = class1.AI(initializers[0])
        self.AI2 = class1.AI(initializers[1])
        self.Player = class1.AI(initializers[2])

          # 初始化 self.stack(以Deck储存Player的回应) 和 self.cache (需要玩家们回应的牌堆)
        self.cache = [class1.Deck(),0]
        self.stack = class1.Deck()

        # 冰山海面上
          # 布局
        panel = wx.Panel(self)
        Vbox_Main = wx.BoxSizer(wx.VERTICAL)
          # 显示历史出牌记录
        hbox0 = wx.BoxSizer()
        self.record = wx.TextCtrl(panel,-1,value='请您先开始：\n',style = wx.TE_MULTILINE,size = (960,200))
        hbox0.Add(self.record, proportion = 1, flag = wx.EXPAND)
        Vbox_Main.Add(hbox0,proportion = 1, flag = wx.TOP|wx.LEFT|wx.RIGHT, border = 20)
        Vbox_Main.Add(-1,10,proportion = 1)
          # 显示玩家当前选择
        hbox1 = wx.BoxSizer()
        self.deck = wx.TextCtrl(panel,-1,style = wx.TE_MULTILINE,size = (960,50))
        hbox1.Add(self.deck, proportion = 0, flag = wx.EXPAND)
        Vbox_Main.Add(hbox1,proportion = 0, flag = wx.LEFT|wx.RIGHT, border = 20)
        Vbox_Main.Add(-1,10,proportion = 1)
          # 显示手牌
        hbox2 = wx.BoxSizer()
        self.hands = wx.TextCtrl(panel,-1,style = wx.TE_MULTILINE,size = (960,50))
        self.hands.SetValue(self.Player.Show)
        hbox2.Add(self.hands, proportion = 0, flag = wx.EXPAND)
        Vbox_Main.Add(hbox2,proportion = 0, flag = wx.LEFT|wx.RIGHT, border = 20)
        Vbox_Main.Add(-1,10,proportion = 1)        
        # 操作台：SPADE   黑桃 9824
        self.buttons = []
        hbox3 = wx.BoxSizer()
        for i in range(13):
            card = class1.Card(i).Show
            button = wx.Button(panel,-1,card,size = (60,20))
            self.Bind(wx.EVT_BUTTON, lambda event,s=card:self.OnButton(event,s),button)
            self.buttons.append(button)
            hbox3.Add(button, flag = wx.RIGHT, border = 10)
        Vbox_Main.Add(hbox3, proportion = 0, flag = wx.ALIGN_CENTER|wx.LEFT, border = 20)
        Vbox_Main.Add(-1,10,proportion = 1)
        # 操作台：BLOSSOM 梅花 9827
        hbox4 = wx.BoxSizer()
        for i in range(13):
            card = class1.Card(i+13).Show
            button = wx.Button(panel,-1,card,size = (60,20))
            self.Bind(wx.EVT_BUTTON, lambda event,s=card:self.OnButton(event,s),button)
            self.buttons.append(button)
            hbox4.Add(button, flag = wx.RIGHT, border = 10)
        Vbox_Main.Add(hbox4, proportion = 0, flag = wx.ALIGN_CENTER|wx.LEFT, border = 20)
        Vbox_Main.Add(-1,10,proportion = 1)
        # 操作台：HEART   红桃 9829
        hbox5 = wx.BoxSizer()
        for i in range(13):
            card = class1.Card(i+26).Show
            button = wx.Button(panel,-1,card,size = (60,20))
            self.Bind(wx.EVT_BUTTON, lambda event,s=card:self.OnButton(event,s),button)
            self.buttons.append(button)
            hbox5.Add(button, flag = wx.RIGHT, border = 10)
        Vbox_Main.Add(hbox5, proportion = 0, flag = wx.ALIGN_CENTER|wx.LEFT, border = 20)
        Vbox_Main.Add(-1,10,proportion = 1)
        # 操作台：PIECE   方片 9830
        hbox6 = wx.BoxSizer()
        for i in range(13):
            card = class1.Card(i+39).Show
            button = wx.Button(panel,-1,card,size = (60,20))
            self.Bind(wx.EVT_BUTTON, lambda event,s=card:self.OnButton(event,s),button)
            self.buttons.append(button)
            hbox6.Add(button, flag = wx.RIGHT, border = 10)
        Vbox_Main.Add(hbox6, proportion = 0, flag = wx.ALIGN_CENTER|wx.LEFT, border = 20)
        Vbox_Main.Add(-1,10,proportion = 1)
        # 操作台：joker & JOKER 大小王
        hbox7 = wx.BoxSizer()
        for i in range(2):
            card = class1.Card(i+52).Show
            button = wx.Button(panel,-1,card,size = (60,20))
            self.Bind(wx.EVT_BUTTON, lambda event,s=card:self.OnButton(event,s),button)
            self.buttons.append(button)
            hbox7.Add(button, flag = wx.RIGHT, border = 10)
        Vbox_Main.Add(hbox7, proportion = 0, flag = wx.ALIGN_CENTER|wx.LEFT, border = 20)
        Vbox_Main.Add(-1,10,proportion = 1)
        # 三个按钮：保存，出牌，托管
        hbox8 = wx.BoxSizer()
        Save = wx.Button(panel,-1,'保存')
        self.Bind(wx.EVT_BUTTON,self.OnSave,Save)
        hbox8.Add(Save, flag = wx.RIGHT, border = 10)
        GiveOut = wx.Button(panel,-1,'出牌')
        self.Bind(wx.EVT_BUTTON,self.OnGiveOut,GiveOut)
        hbox8.Add(GiveOut, flag = wx.RIGHT, border = 10)
        Pass = wx.Button(panel,-1,'跳过')
        self.Bind(wx.EVT_BUTTON,self.OnPass,Pass)
        hbox8.Add(Pass, flag = wx.RIGHT, border = 10)
        Vbox_Main.Add(hbox8, proportion = 0, flag = wx.ALIGN_CENTER|wx.LEFT|wx.BOTTOM, border = 20)

        panel.SetSizer(Vbox_Main)

    # 出牌
    def OnGiveOut(self,event):
        # 检查自身
        PlayerOutput = self.stack
        if PlayerOutput.Type == -1:
            return
        elif PlayerOutput.Type == 11:
            dlg = wx.MessageDialog(self,'您的出牌是无效类型。','提示')
            dlg.ShowModal()
            dlg.Destroy()
            return
        elif PlayerOutput.Type == 10:
            if self.cache[0].Type != 10:
                #替换self.cache[0]/从self.Player中GiveOut/进行胜利判定（self.Player’空‘了没有）
                self.cache[0] = class1.Deck(PlayerOutput.indexs)
                self.cache[1] = 0
                self.stack = class1.Deck()
                self.Player.GiveOut(self.cache[0].cards)
                if self.Player.isEmpty():
                    dlg = wx.MessageDialog(self,'您胜利了','祝贺')
                    dlg.ShowModal()
                    dlg.Destroy()
                    del self.AI1
                    del self.AI2
                    return
                else:
                    pass
            else:
                if self.cache[0].ComparableKey >= PlayerOutput.ComparableKey:
                    dlg = wx.MessageDialog(self,'您不能这样出牌。','提示')
                    dlg.ShowModal()
                    dlg.Destroy()
                    return
                else:
                    #替换self.cache[0]/从self.Player中GiveOut/进行胜利判定（self.Player’空‘了没有）
                    self.cache[0] = class1.Deck(PlayerOutput.indexs)
                    self.cache[1] = 0
                    self.stack = class1.Deck()
                    self.Player.GiveOut(self.cache[0].cards)
                    if self.Player.isEmpty():
                        dlg = wx.MessageDialog(self,'您胜利了','祝贺')
                        dlg.ShowModal()
                        dlg.Destroy()
                        del self.AI1
                        del self.AI2
                        return
                    else:
                        pass
        elif PlayerOutput.Type >= 0 and PlayerOutput.Type <= 7:
            if self.cache[0].Type != PlayerOutput.Type:
                if self.cache[0].Type != -1:
                    dlg = wx.MessageDialog(self,'您的出牌与上家的类型不一致。','提示')
                    dlg.ShowModal()
                    dlg.Destroy()
                    return
                else:
                    #替换self.cache[0]/从self.Player中GiveOut/进行胜利判定（self.Player’空‘了没有）
                    self.cache[0] = class1.Deck(PlayerOutput.indexs)
                    self.cache[1] = 0
                    self.stack = class1.Deck()
                    self.Player.GiveOut(self.cache[0].cards)
                    if self.Player.isEmpty():
                        dlg = wx.MessageDialog(self,'您胜利了','祝贺')
                        dlg.ShowModal()
                        dlg.Destroy()
                        del self.AI1
                        del self.AI2
                        return
                    else:
                        pass
            else:
                if self.cache[0].ComparableKey >= PlayerOutput.ComparableKey:
                    dlg = wx.MessageDialog(self,'您的出牌压不住上家。','提示')
                    dlg.ShowModal()
                    dlg.Destroy()
                    return
                else:
                    #替换self.cache[0]/从self.Player中GiveOut/进行胜利判定（self.Player’空‘了没有）
                    self.cache[0] = class1.Deck(PlayerOutput.indexs)
                    self.cache[1] = 0
                    self.stack = class1.Deck()
                    self.Player.GiveOut(self.cache[0].cards)
                    if self.Player.isEmpty():
                        dlg = wx.MessageDialog(self,'您胜利了','祝贺')
                        dlg.ShowModal()
                        dlg.Destroy()
                        del self.AI1
                        del self.AI2
                        return
                    else:
                        pass
        else:
            if self.cache[0].Type != PlayerOutput.Type:
                if self.cache[0].Type != -1:
                    dlg = wx.MessageDialog(self,'您的出牌与上家的类型不一致。','提示')
                    dlg.ShowModal()
                    dlg.Destroy()
                    return
                else:
                   #替换self.cache[0]/从self.Player中GiveOut/进行胜利判定（self.Player’空‘了没有）
                    self.cache[0] = class1.Deck(PlayerOutput.indexs)
                    self.cache[1] = 0
                    self.stack = class1.Deck()
                    self.Player.GiveOut(self.cache[0].cards)
                    if self.Player.isEmpty():
                        dlg = wx.MessageDialog(self,'您胜利了','祝贺')
                        dlg.ShowModal()
                        dlg.Destroy()
                        del self.AI1
                        del self.AI2
                        return 
                    else:
                        pass
            else:
                if self.cache[0].ComparableKey[0] != PlayerOutput.ComparableKey[0]:
                    dlg = wx.MessageDialog(self,'您不能这样出牌。','提示')
                    dlg.ShowModal()
                    dlg.Destroy()
                    return
                else:
                    if self.cache[0].ComparableKey[1] >= PlayerOutput.ComparableKey[1]:
                        dlg = wx.MessageDialog(self,'您不能这样出牌。','提示')
                        dlg.ShowModal()
                        dlg.Destroy()
                        return
                    else:
                        #替换self.cache[0]/从self.Player中GiveOut/进行胜利判定（self.Player’空‘了没有）
                        self.cache[0] = class1.Deck(PlayerOutput.indexs)
                        self.cache[1] = 0
                        self.stack = class1.Deck()
                        self.Player.GiveOut(self.cache[0].cards)
                        if self.Player.isEmpty():
                            dlg = wx.MessageDialog(self,'您胜利了','祝贺')
                            dlg.ShowModal()
                            dlg.Destroy()
                            del self.AI1
                            del self.AI2
                            return
                        else:
                            pass
        self.record.SetValue(self.record.Value+'\nYou: '+self.cache[0].Show)
        self.hands.SetValue(self.Player.Show)

        # AI互搏，过程显示在self.record中。
        AI1_response = self.AI1.Response(self.cache[0])

        if AI1_response == -1:
            self.record.SetValue(self.record.Value+'\nAI1 Pass')
            self.cache[1] += 1
            if self.cache[1] >= 2:
                self.cache = [class1.Deck(),0]
        else:
            #替换self.cache[0]/从self.Player中GiveOut/进行胜利判定（self.Player’空‘了没有）
            self.cache[0] = class1.Deck(AI1_response.indexs)
            self.cache[1] = 0
            self.stack = class1.Deck()
            self.AI1.GiveOut(self.cache[0].cards)
            if self.AI1.isEmpty():
                dlg = wx.MessageDialog(self,'AI1胜利了。\nNice Playing with you two! So exicting! I am a good bot, right?','祝贺')
                dlg.ShowModal()
                dlg.Destroy()
                del self.Player
                del self.AI2
                return
            self.record.SetValue(self.record.Value+'\nAI1: '+self.cache[0].Show)

        AI2_response = self.AI2.Response(self.cache[0])

        if AI2_response == -1:
            self.record.SetValue(self.record.Value+'\nAI2 Pass')
            self.cache[1] += 1
            if self.cache[1] >= 2:
                self.cache = [class1.Deck(),0]
        else:
            #替换self.cache[0]/从self.Player中GiveOut/进行胜利判定（self.Player’空‘了没有）
            self.cache[0] = class1.Deck(AI2_response.indexs)
            self.cache[1] = 0
            self.stack = class1.Deck()
            self.AI2.GiveOut(self.cache[0].cards)
            if self.AI2.isEmpty():
                dlg = wx.MessageDialog(self,'AI2胜利了。\nNice Playing with you two! So exicting! I am a good bot, right?','祝贺')
                dlg.ShowModal()
                dlg.Destroy()
                del self.Player
                del self.AI1
                return
            self.record.SetValue(self.record.Value+'\nAI2: '+self.cache[0].Show)
    
    # 跳过回合
    def OnPass(self,event):
        self.record.SetValue(self.record.Value+'\nPlayer Pass')
        self.cache[1] += 1
        if self.cache[1] >= 2:
            self.cache = [class1.Deck(),0]

        # AI互搏，过程显示在self.record中。
        AI1_response = self.AI1.Response(self.cache[0])

        if AI1_response == -1:
            self.record.SetValue(self.record.Value+'\nAI1 Pass')
            self.cache[1] += 1
            if self.cache[1] >= 2:
                self.cache = [class1.Deck(),0]
        else:
            #替换self.cache[0]/从self.Player中GiveOut/进行胜利判定（self.Player’空‘了没有）
            self.cache[0] = class1.Deck(AI1_response.indexs)
            self.cache[1] = 0
            self.stack = class1.Deck()
            self.AI1.GiveOut(self.cache[0].cards)
            if self.AI1.isEmpty():
                dlg = wx.MessageDialog(self,'AI1胜利了。\nNice Playing with you two! So exicting! I am a good bot, right?','祝贺')
                dlg.ShowModal()
                dlg.Destroy()
                del self.Player
                del self.AI2
                return
            self.record.SetValue(self.record.Value+'\nAI1: '+self.cache[0].Show)

        AI2_response = self.AI2.Response(self.cache[0])

        if AI2_response == -1:
            self.record.SetValue(self.record.Value+'\nAI2 Pass')
            self.cache[1] += 1
            if self.cache[1] >= 2:
                self.cache = [class1.Deck(),0]
        else:
            #替换self.cache[0]/从self.Player中GiveOut/进行胜利判定（self.Player’空‘了没有）
            self.cache[0] = class1.Deck(AI2_response.indexs)
            self.cache[1] = 0
            self.stack = class1.Deck()
            self.AI2.GiveOut(self.cache[0].cards)
            if self.AI2.isEmpty():
                dlg = wx.MessageDialog(self,'AI2胜利了。\nNice Playing with you two! So exicting! I am a good bot, right?','祝贺')
                dlg.ShowModal()
                dlg.Destroy()
                del self.Player
                del self.AI1
                return
            self.record.SetValue(self.record.Value+'\nAI2: '+self.cache[0].Show)


    # 操作缓冲区。（要出的牌）
    def OnButton(self,event,s):
        index = class1.getIndex(s)
        if index not in self.Player.indexs:
            return
        if index in self.stack.indexs:
            self.stack.GiveOut(index)
        else:
            self.stack.Add(index)
        self.deck.SetValue(self.stack.Show)

    # 保存结果的方法
    def OnSave(self,event):
        dlg = wx.DirDialog(self,'保存游戏记录')
        if dlg.ShowModal() == wx.ID_OK:
            file_index = hex(random.randint(0,100))
            dir = dlg.GetPath()
            filename = 'Game Record {}.txt'.format(file_index)
            with open(os.path.join(dir,filename),'w') as f:
                f.write(self.record.GetValue())
        dlg.Destroy()

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()
