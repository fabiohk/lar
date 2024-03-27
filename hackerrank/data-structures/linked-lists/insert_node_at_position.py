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

def insertNodeAtPosition(llist, data, position):
    new_node = SinglyLinkedListNode(data)
    
    if llist is None:
        return new_node
    
    head = llist
    previous_node, node_to_be_moved = None, llist
    
    for _ in range(position):
        previous_node, node_to_be_moved = node_to_be_moved, node_to_be_moved.next
        if node_to_be_moved is None:
            break
        
    if previous_node is not None:
        previous_node.next = new_node
    if node_to_be_moved is not None:
        new_node.next = node_to_be_moved
        
    return head if position > 0 else new_node