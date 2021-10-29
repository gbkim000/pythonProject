# Linked List

class Node:
    def __init__(self, value):
        self.val = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def mprint(self):
        printVal = self.head
        while printVal is not None:
            print(printVal.val)
            printVal = printVal.next

    def addFirst(self, value):
        addedNode = Node(value)
        addedNode.next = self.head
        self.head = addedNode

    def addLast(self, value):
        LListM = self.head
        while LListM.next:
            LListM = LListM.next
        addedNode = Node(value)
        LListM.next = addedNode

    def removeNode(self, data):
        headVal = self.head
        if headVal is not None:
            if headVal.val == data:
                self.head = headVal.next
                headVal = None
                return
        while headVal is not None:
            if headVal.val == data:
                break
            prev = headVal
            headVal = headVal.next
        if headVal is None:
            return
        prev.next = headVal.next
        headVal = None
        
LList = LinkedList()
LList.head = Node("LNode1")
Node2 = Node("LNode2")
Node3 = Node("LNode3")
LList.head.next = Node2
Node2.next = Node3
LList.addFirst("LNode4")
LList.addLast("LNode5")
LList.removeNode("LNode2")
LList.mprint()
