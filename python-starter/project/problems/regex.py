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
            p1 = re.compile(r'^\d{2}-15\b')
            p2 = re.compile(r'^\d{2}-15\b\s+10:18:51')
            p3 = re.compile(r'^\S+\s+\d{2}:\d{2}:51')
            p4 = re.compile(r'^\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+.*\blowmemorykiller\b')
            p5 = re.compile(r'^\S+\s+10:18:51\b\s+221\b')
            p6 = re.compile(r'^\S+\s+\S+\s+\S+\s+\S+\s+E\b')
            p7 = re.compile(r'^\S+\s+\S+\s+\S+\s+\S+\s+W\s+PackageManager\b')
            p8 = re.compile(r'^\S+\s+\S+\s+\S+\s+\S+\s+D\s+.*?\bExoPlayer\b')
            p9 = re.compile(r'^\S+\s+\S+\s+\S+\s+\S+\s+[EW]\s+.*?\b[\w_-]+\.java:')
            p10 = re.compile(r'^([0-9-]+)\s+([0-9:]+)\s+(\d+)\s+(\d+)\s+([IDVEFAW])\s+([^:]+?):\s+.*\bThread\b')

            c1 = c2 = c3 = c4 = c5 = c6 = c7 = c8 = c9 = c10 = 0

            for line in lines:
                stripped = line.strip()
                if p1.match(stripped): c1 += 1
                if p2.match(stripped): c2 += 1
                if p3.match(stripped): c3 += 1
                if p4.search(stripped): c4 += 1
                if p5.match(stripped): c5 += 1
                if p6.match(stripped): c6 += 1
                if p7.match(stripped): c7 += 1
                if p8.match(stripped): c8 += 1
                if p9.match(stripped): c9 += 1
                if p10.match(stripped): c10 += 1

            output_lines = [str(c1), str(c2), str(c3), str(c4), str(c5), str(c6), str(c7), str(c8), str(c9), str(c10)]

        elif rgx_task == 2:
            java_file_pattern = re.compile(r'([\w_-]+\.java)(?::\d+)?')
            for line in lines:
                stripped = line.strip()
                m = log_pattern.match(stripped)
                if m:
                    _, _, _, _, level, _, message = m.groups()
                    if level == 'E' and message:
                        matches = java_file_pattern.findall(message)
                        for match in matches:
                            output_lines.append(match)
                else:
                    matches = java_file_pattern.findall(stripped)
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
                output_lines = [f"{max_pid}={max_count} ({max_count} errors)"]
            else:
                output_lines = ["0=0 (0 errors)"]

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