class SinglyLinkedListNode:
    def __init__(self, node_data):
        self.data = node_data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_node(self, node_data):
        node = SinglyLinkedListNode(node_data)

        if not self.head:
            self.head = node
        else:
            self.tail.next = node


        self.tail = node

def getNode(llist, positionFromTail):
    values = []
    
    while llist is not None:
        values.append(llist.data)
        llist = llist.next
        
    return values[-positionFromTail-1]