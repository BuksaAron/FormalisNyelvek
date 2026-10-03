from project.problem import Problem
import argparse

class DVAProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--check', help='Ellenorizendo szavak', type=str)
    
    def is_chosen_problem(self, args):
        return args.check is not None

    def run(self, args):
        in_file = args.input
        out_file = args.output

        if not args.check:
            words = []
        else:
            words = args.check.split(',')

        with open(in_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        states = lines[0].split()
        alphabet = lines[1].split()
        start = lines[2]
        accept_states = set(lines[3].split())

        transitions = {}
        for line in lines[4:]:
            parts = line.split()
            if len(parts) == 3:
                state, symbol, next_state = parts
                transitions[(state, symbol)] = next_state
            
        results = []
        for word in words:
            current_state = start
            accepted = True

            for symbol in word:
                if (current_state, symbol) in transitions:
                    current_state = transitions[(current_state, symbol)]
                else:
                    accepted = False
                    break
            
            if accepted and current_state in accept_states:
                results.append("IGEN")
            else:
                results.append("NEM")

        with open(out_file, 'w') as f:
            f.write('\n'.join(results) + '\n')
