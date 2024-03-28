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

def removeDuplicates(llist):
    values_map = {}
    
    while llist is not None:
        if llist.data not in values_map:
            values_map[llist.data] = True
        llist = llist.next
    
    sorted_values = sorted(values_map.keys())
    current_node = head = SinglyLinkedListNode(sorted_values[0])
    for value in sorted_values[1:]:
        new_node = SinglyLinkedListNode(value)
        current_node.next = new_node
        current_node = new_node
    
    return head