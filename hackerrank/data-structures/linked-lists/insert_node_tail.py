class SinglyLinkedListNode:
    def __init__(self, node_data):
        self.data = node_data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

def insertNodeAtTail(head, data):
    if head is None:
        return SinglyLinkedListNode(data)
    
    node = head
    
    while node.next is not None:
        node = node.next
    node.next = SinglyLinkedListNode(data)
    
    return head