class SLNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class SLStack:
    def __init__(self):
        # "head" ganti nama jadi top
        self.top = None

    def is_empty(self):
        if self.top == None:
            return True
        else:
            return False

    def push(self, newdata):
        newnode = SLNode(newdata)
        newnode.next = self.top
        self.top = newnode

    def peek(self):
        if self.is_empty():
            print("Error peek: stack sedang kosong.")
        else:
            return self.top.data

    def pop(self):
        if self.is_empty():
            print("Error pop: stack sudah kosong sebelumnya.")
        else:
            output = self.top.data
            temp = self.top
            self.top = self.top.next
            del temp
            return output

    def get_size(self):
        temp = self.top
        size = 0
        while temp != None:
            size += 1
            temp = temp.next
        return size

    # output print stacknya diubah jd bentuk list untuk mempermudah visual
    def print_stack(self):
        temp = self.top
        stack_list = []
        while temp != None:
            stack_list.append(temp.data)
            temp = temp.next
        print(f"Stack: {stack_list}\n")

    # print linked list
    def print_storage(self):
        print("top -> ", end="")
        temp = self.top
        while temp != None:
            print(temp.data, end=" -> ")
            temp = temp.next
        print("None")
