class SinglyLinkedListNode:
    def __init__(self, node_data):
        self.data = node_data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

def insertNodeAtHead(llist, data):
    if llist is None:
        return SinglyLinkedListNode(data)
        
    new_head = SinglyLinkedListNode(data)
    new_head.next = llist
    return new_head