from project.problem import Problem
import argparse

class MinimizationProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--mini', help='Automaták minimizálása', action='store_true')

    def is_chosen_problem(self, args):
        return bool(args.mini)

    def run(self, args):
        in_file = args.input
        out_file = args.output

        with open(in_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        valid_states = set(lines[0].split())
        alphabet = lines[1].split()
        start_state = lines[2]
        accept_states = set(lines[3].split())

        transitions_raw = {}
        for line in lines[4:]:
            parts = line.split()
            if len(parts) == 3:
                src, symbol, dst = parts
                if src not in valid_states or dst not in valid_states or symbol not in alphabet:
                    raise ValueError(f"Hiba: Érvénytelen állapot vagy szimbólum az átmenetben: {line}")
                transitions_raw[(src, symbol)] = dst

        reachable = set()
        queue = [start_state]
        reachable.add(start_state)
        while queue:
            curr = queue.pop(0)
            for sym in alphabet:
                if (curr, sym) in transitions_raw:
                    nxt = transitions_raw[(curr, sym)]
                    if nxt not in reachable:
                        reachable.add(nxt)
                        queue.append(nxt)

        states = sorted(list(reachable), key=lambda x: int(x[1:]))
        accept_states = accept_states.intersection(states)

        marked = {}
        states_list = states
        n = len(states_list)

        for i in range(n):
            for j in range(i + 1, n):
                s1 = states_list[i]
                s2 = states_list[j]
                if (s1 in accept_states) != (s2 in accept_states):
                    marked[(s1, s2)] = True
                    marked[(s2, s1)] = True
                else:
                    marked[(s1, s2)] = False
                    marked[(s2, s1)] = False

        changed = True
        while changed:
            changed = False
            for i in range(n):
                for j in range(i + 1, n):
                    s1 = states_list[i]
                    s2 = states_list[j]
                    if not marked[(s1, s2)]:
                        for sym in alphabet:
                            t1 = transitions_raw.get((s1, sym))
                            t2 = transitions_raw.get((s2, sym))
                            if t1 and t2 and marked.get((t1, t2), False):
                                marked[(s1, s2)] = True
                                marked[(s2, s1)] = True
                                changed = True
                                break
                            elif (t1 is None) != (t2 is None):
                                marked[(s1, s2)] = True
                                marked[(s2, s1)] = True
                                changed = True
                                break

        parent = {s: s for s in states_list}   
        def find(s):
            if parent[s] != s:
                parent[s] = find(parent[s])
                s = parent[s]
            return s

        def union(s1, s2): 
            root1 = find(s1)
            root2 = find(s2)
            if root1 != root2:
                if int(root1[1:]) < int(root2[1:]):
                    parent[root2] = root1
                else:
                    parent[root1] = root2

        for i in range(n):
            for j in range(i + 1, n):
                s1 = states_list[i]
                s2 = states_list[j]
                if not marked[(s1, s2)]:
                    union(s1, s2)

        classes = {}
        for s in states_list:
            root = find(s)
            if root not in classes:
                classes[root] = []
            classes[root].append(s)

        state_mapping = {}
        new_states = []
        for root in sorted(classes.keys(), key=lambda x: int(x[1:])):
            new_name = f"s{root[1:]}"
            new_states.append(new_name)
            for member in classes[root]:
                state_mapping[member] = new_name

        new_start = state_mapping[start_state]

        new_accept_states = set()
        for acc in accept_states:
            if acc in state_mapping:
                new_accept_states.add(state_mapping[acc])
        new_accept_states = sorted(list(new_accept_states), key=lambda x: int(x[1:]))

        new_transitions_set = set()
        for s in states_list:
            new_src = state_mapping[s]
            for sym in alphabet:
                if (s, sym) in transitions_raw:
                    target = transitions_raw[(s, sym)]
                    new_dst = state_mapping[target]
                    new_transitions_set.add((new_src, sym, new_dst))

        new_transitions = list(new_transitions_set)
        new_transitions.sort(key=lambda t: (int(t[0][1:]), t[1], int(t[2][1:])))

        output_lines = [
            " ".join(new_states),
            " ".join(alphabet),
            new_start,
            " ".join(new_accept_states)
        ]
        for src, sym, dst in new_transitions:
            output_lines.append(f"{src} {sym} {dst}")

        with open(out_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_lines) + "\n")