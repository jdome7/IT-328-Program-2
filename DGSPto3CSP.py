import sys
import subprocess

# read DGSP input
def read_input(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    vertices = list(map(int, lines[0].split()))
    n = len(vertices)

    adj = []
    for i in range(1, n + 1):
        adj.append(list(map(int, lines[i].split())))

    u, v = map(int, lines[n + 1].split())
    l = int(lines[n + 2])

    return n, adj, u, v, l

# color cycle
def color_of(i):
    if i % 3 == 0:
        return "b"
    elif i % 3 == 1:
        return "w"
    else:
        return "r"

# build layered graph
def build_G(n, adj, u, v, l):
    G_vertices = []
    G_edges = []

    for x in range(1, n + 1):
        for i in range(l + 1):
            G_vertices.append((x, i))

    for x in range(1, n + 1):
        for y in range(1, n + 1):
            if adj[x - 1][y - 1] == 1:
                for i in range(l):
                    G_edges.append(((x, i), (y, i + 1)))

    p1 = ("p1", 0)
    p2 = ("p2", 0)
    G_vertices.append(p1)
    G_vertices.append(p2)

    for i in range(l + 1):
        G_edges.append(((v, i), p1))
        G_edges.append((p1, (v, i)))
        G_edges.append(((v, i), p2))
        G_edges.append((p2, (v, i)))

    t_color = color_of(l + 1)
    t = ("t", 0)
    G_vertices.append(t)

    predecessor = {"b": "r", "w": "b", "r": "w"}[t_color]

    for i in range(l + 1):
        if color_of(i) == predecessor:
            G_edges.append(((v, i), t))

    k = l + 3

    return G_vertices, G_edges, t_color, k, u

# build output text
def build_output_text(G_vertices, G_edges, t_color, k, u):
    id_map = {}
    counter = 1
    for v in G_vertices:
        id_map[v] = counter
        counter += 1

    size = len(G_vertices)
    matrix = [[0] * size for _ in range(size)]
    for (a, b) in G_edges:
        matrix[id_map[a] - 1][id_map[b] - 1] = 1

    lines = []

    vertex_parts = []
    for v in G_vertices:
        if v[0] == "t":
            vertex_parts.append(f"{id_map[v]}{t_color}")
        elif v[0] == "p1":
            vertex_parts.append(f"{id_map[v]}w")
        elif v[0] == "p2":
            vertex_parts.append(f"{id_map[v]}r")
        else:
            vertex_parts.append(f"{id_map[v]}{color_of(v[1])}")
    lines.append(" ".join(vertex_parts))

    for row in matrix:
        lines.append(" ".join(map(str, row)))

    s_id = id_map[(u, 0)]
    t_id = id_map[("t", 0)]
    lines.append(f"{s_id} {t_id}")

    lines.append(str(k))

    return "\n".join(lines)

# transform DGSP to 3CSP
def transform(filename):
    n, adj, u, v, l = read_input(filename)
    G_vertices, G_edges, t_color, k, u = build_G(n, adj, u, v, l)
    out_text = build_output_text(G_vertices, G_edges, t_color, k, u)
    return out_text

# main
def main():
    if len(sys.argv) != 2:
        print("Usage: python DGSPto3CSP.py <input_file>")
        return

    input_file = sys.argv[1]

    out_text = transform(input_file)

    print("=== Transformed 3CSP instance ===")
    print(out_text)
    print("=== End of instance ===")

    with open("temp.txt", "w") as f:
        f.write(out_text)

    print("\nWrote transformed instance to temp.txt")
    print("Running 3csp.py on temp.txt\n")

    subprocess.run([sys.executable, "3csp.py", "temp.txt"])

if __name__ == "__main__":
    main()
