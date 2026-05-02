# IT 328 Project 2, By: Marcos Avila and Josiah Domercant

from collections import deque

def solve_3csp(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    

    vertex_info = lines[0].split()
    node_color_map = {}
    for item in vertex_info:
        # generative AI was used in the line below to assist in writing code to extract vertex ID and color
        v = int(''.join(filter(str.isdigit, item)))
        color = item[-1].lower()
        node_color_map[v] = color

    num_vertices = len(node_color_map)
    
    # parsing adjacency matrix to make 2d list
    adj_matrix = []
    for i in range(1, 1 + num_vertices):
        adj_matrix.append(list(map(int, lines[i].split())))

 
    s, t = map(int, lines[1 + num_vertices].split())
    k = int(lines[2 + num_vertices])

    patterns = [
        {'b': 'w', 'w': 'r', 'r': 'b'},
        {'b': 'r', 'r': 'w', 'w': 'b'}
    ]

    def bfs(next_color_map):
        # store current node and the list path taken to reach it
        queue = deque([(s, [s])])
        # store currrent node and path length
        visited = set([(s, 0)]) 

        while queue:
            curr_node, path = queue.popleft()
            
            if len(path) - 1 > k:
                continue
            
            if curr_node == t:
                return path

            curr_color = node_color_map[curr_node]
            required_next_color = next_color_map[curr_color]

            # generative AI was used in the line below in the for loop condition to assist in checking neighbors in the adjacency matrix
            for neighbor_idx, is_connected in enumerate(adj_matrix[curr_node - 1]):
                neighbor_id = neighbor_idx + 1
                if is_connected:
                    if node_color_map[neighbor_id] == required_next_color:
                        state = (neighbor_id, len(path))
                        if state not in visited and len(path) <= k:
                            visited.add(state)
                            queue.append((neighbor_id, path + [neighbor_id]))
        return None

    # run BFS for both patterns
    for pattern in patterns:
        result_path = bfs(pattern)
        if result_path:
            print("Accept")
            print(f"Path: {' -> '.join(map(str, result_path))}")
            return

    print("Reject")


while True:     
    user_input = input("\n1 - New file \n2 - Exit\n")

    if user_input.lower() == '2':
        break
    else: 
        filename = input("Enter the filename:\n")
        with open(filename, 'r') as f:
            print(f.read())
        solve_3csp(filename)
