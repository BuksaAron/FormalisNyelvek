from project.problem import Problem
import argparse
import re

class RegexProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--rgx', help='Logfájl elemzése reguláris kifejezésekkel (1-5)', type=int)

    def is_chosen_problem(self, args):
        return args.rgx is not None

    def run(self, args):
        in_file = args.input
        out_file = args.output
        rgx_task = args.rgx

        with open(in_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        log_pattern = re.compile(r'^([0-9-]+)\s+([0-9:]+)\s+(\d+)\s+(\d+)\s+([IDVEFAW])\s+([^:]+?):\s*(.*)?')

        output_lines = []

        if rgx_task == 1:
            c1 = c2 = c3 = c4 = c5 = c6 = c7 = c8 = c9 = c10 = 0
            
            for line in lines:
                m = log_pattern.match(line.strip())
                if not m:
                    continue
                date, time_str, pid, tid, level, tag, message = m.groups()
                message = message if message else ""

                if '10-15' in date:
                    c1 += 1
                
                if '10-15' in date and time_str.startswith('10:18:51'):
                    c2 += 1
                
                if ':51' in time_str:
                    c3 += 1
                
                if 'lowmemorykiller' in tag:
                    c4 += 1
                
                if time_str.startswith('10:18:51') and pid == '221':
                    c5 += 1
                
                if level == 'E':
                    c6 += 1
                
                if level == 'W' and tag.strip() == 'PackageManager':
                    c7 += 1
                
                if level == 'D' and ('ExoPlayer' in tag or 'ExoPlayer' in message):
                    c8 += 1
                
                if level in ('E', 'W') and '.java:' in message:
                    c9 += 1
                
                if 'Thread' in message:
                    c10 += 1

            output_lines = [str(c1), str(c2), str(c3), str(c4), str(c5), str(c6), str(c7), str(c8), str(c9), str(c10)]

        elif rgx_task == 2:
            java_file_pattern = re.compile(r'([\w_-]+\.java)(?::\d+)?')
            for line in lines:
                m = log_pattern.match(line.strip())
                if m:
                    _, _, _, _, level, _, message = m.groups()
                    if level == 'E' and message:
                        matches = java_file_pattern.findall(message)
                        for match in matches:
                            output_lines.append(match)

        elif rgx_task == 3:
            seen_pids = []
            for line in lines:
                m = log_pattern.match(line.strip())
                if m:
                    _, _, pid, _, _, _, _ = m.groups()
                    if pid not in seen_pids:
                        seen_pids.append(pid)
            output_lines = seen_pids

        elif rgx_task == 4:
            error_counts = {}
            for line in lines:
                m = log_pattern.match(line.strip())
                if m:
                    _, _, pid, _, level, _, _ = m.groups()
                    if level == 'E':
                        error_counts[pid] = error_counts.get(pid, 0) + 1
            if error_counts:
                max_pid = max(error_counts, key=error_counts.get)
                max_count = error_counts[max_pid]
                output_lines = [f"${max_pid}={max_count}$ ({max_count} errors)"]
            else:
                output_lines = ["$0=0$ (0 errors)"]

        elif rgx_task == 5:
            main_thread_errors = 0
            for line in lines:
                m = log_pattern.match(line.strip())
                if m:
                    _, _, pid, tid, level, _, _ = m.groups()
                    if level == 'E' and pid == tid:
                        main_thread_errors += 1
            output_lines = [str(main_thread_errors)]

        with open(out_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_lines) + "\n")