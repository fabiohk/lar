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

def deleteNode(llist, position):
    if llist is None:
        return llist
        
    if position == 0:
        return llist.next
        
    head = llist
    previous_node, node_to_be_removed = None, llist
    for _ in range(position):
        previous_node, node_to_be_removed = node_to_be_removed, node_to_be_removed.next
            
    previous_node.next = node_to_be_removed.next
    return head