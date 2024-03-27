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

def reverse(llist):
    if llist is None:
        return llist
        
    if llist.next is None:
        return llist
        
    previous, current, next_node = None, llist, llist.next
    while next_node is not None:
        current.next = previous
        previous, current, next_node = current, next_node, next_node.next
    current.next = previous
    return current