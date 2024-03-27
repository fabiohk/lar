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

def reversePrint(llist):
    llist_values = []
    
    while llist is not None:
        llist_values.append(llist.data)
        llist = llist.next
        
    for data in llist_values[::-1]:
        print(data)