from sortedcontainers import SortedList

def breadth_search (start, end, possible_paths, travel_path, search_depth, heuristic=None, represent=None, return_table=None):

    class Node:

        def __init__ (self, state, parent, path, depth):
            self.state = state
            self.parent = parent
            self.path = path
            self.depth = depth

    class QueueValue:

        def __init__ (self, state):
            self.state = state
            self.rep = state if not represent else represent(state)
            self.heuristic = 0 if not heuristic else heuristic(self.rep)

        def __lt__ (self, other):
            if heuristic:
                return self.heuristic < other.heuristic
            else:
                return seen_states[self.rep].depth < seen_states[other.rep].depth
            

    queue_start = QueueValue(start)
    seen_states = { queue_start.rep : Node(queue_start.state, None, None, 0) }
    queue = SortedList([queue_start])

    if queue_start.rep == end:
        return []
    
    while queue:

        current = queue.pop(0)
        for path in possible_paths:
            new_state = travel_path(current.state, path)
            new_queue_value = QueueValue(new_state)
            new_rep = new_queue_value.rep

            if new_rep == end:
                solution = [path]
                previous = current.rep
                while seen_states[previous].parent:
                    solution.append(seen_states[previous].path)
                    previous = seen_states[previous].parent
                return solution[::-1]
            
            if new_rep not in seen_states and seen_states[current.rep].depth < search_depth-1:
                seen_states[new_rep] = Node(new_state, current.rep, path, seen_states[current.rep].depth+1)
                queue.add(new_queue_value)

    if return_table:
        return seen_states

    return "No solution found"