class Node:
    def __init__(self, value):
        self.val = value
        self.next = None

class SLinkedList:
    def __init__(self):
        self.head = None

    def mprint(self):
        printval = self.head
        while printval is not None:
            print(printval.val)
            printval = printval.next

    def AddFirst(self, nvalue):
        addedNode = Node(nvalue)
        addedNode.next = self.head
        self.head = addedNode

    def AddLast(self, nvalue):
        LListM = self.head
        while (LListM.next):
            LListM = LListM.next
        addedNode = Node(nvalue)
        LListM.next = addedNode

    def RemoveNode(self, Rdata):
        HeadVal = self.head
        if (HeadVal is not None):
            if (HeadVal.val == Rdata):
                self.head = HeadVal.next
                HeadVal = None
                return
        while (HeadVal is not None):
            if HeadVal.val == Rdata:
                break
            prev = HeadVal
            HeadVal = HeadVal.next
        if (HeadVal == None):
            return
        prev.next = HeadVal.next
        HeadVal = None
        
LList = SLinkedList()
LList.head = Node("LNode1")
Node2 = Node("LNode2")
Node3 = Node("LNode3")
LList.head.next = Node2
Node2.next = Node3
LList.AddFirst("LNode4")
LList.AddLast("LNode5")
LList.RemoveNode("LNode2")
LList.mprint()
