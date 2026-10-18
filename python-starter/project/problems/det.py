from project.problem import Problem
import argparse

class DeterminizationProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--det', help='Automaták determinizálása', action='store_true')

    def is_chosen_problem(self, args):
        return bool(args.det)

    def run(self, args):
        in_file = args.input
        out_file = args.output

        with open(in_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        valid_states = set(lines[0].split())
        alphabet = lines[1].split()
        start_state = lines[2]
        accept_states = set(lines[3].split())

        transitions_raw = []
        for line in lines[4:]:
            parts = line.split()
            if len(parts) == 3:
                src, symbol, dst = parts
                if src not in valid_states or dst not in valid_states or symbol not in alphabet:
                    raise ValueError(f"Hiba: Érvénytelen állapot vagy szimbólum az átmenetben: {line}")
                transitions_raw.append((src, symbol, dst))

        initial_subset = frozenset([start_state])
        
        subset_to_name = {initial_subset: "s0"}
        name_to_subset = {"s0": initial_subset}
        queue = [initial_subset]
        
        dfa_transitions = []

        while queue:
            current_subset = queue.pop(0)
            current_name = subset_to_name[current_subset]

            for symbol in alphabet:
                next_subset_states = set()
                for state in current_subset:
                    for src, sym, dst in transitions_raw:
                        if src == state and sym == symbol:
                            next_subset_states.add(dst)
                
                if next_subset_states:
                    next_subset = frozenset(next_subset_states)
                    if next_subset not in subset_to_name:
                        new_name = f"s{len(subset_to_name)}"
                        subset_to_name[next_subset] = new_name
                        name_to_subset[new_name] = next_subset
                        queue.append(next_subset)
                    
                    target_name = subset_to_name[next_subset]
                    dfa_transitions.append((current_name, symbol, target_name))

        dfa_states = sorted(list(name_to_subset.keys()), key=lambda x: int(x[1:]))

        dfa_accept_states = []
        for name in dfa_states:
            subset = name_to_subset[name]
            if any(acc in subset for acc in accept_states):
                dfa_accept_states.append(name)

        dfa_transitions.sort(key=lambda t: (int(t[0][1:]), t[1], int(t[2][1:])))

        output_lines = [
            " ".join(dfa_states),
            " ".join(alphabet),
            "s0",
            " ".join(dfa_accept_states)
        ]
        for src, sym, dst in dfa_transitions:
            output_lines.append(f"{src} {sym} {dst}")

        with open(out_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_lines) + "\n")