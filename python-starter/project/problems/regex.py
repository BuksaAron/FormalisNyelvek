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

        log_pattern = re.compile(
            r'^([0-9-]+)\s+([0-9:.]+)\s+(\d+)\s+(\d+)\s+([IDVEFAW])\s+([^:]+?):(?:\s+(.*))?'
        )

        output_lines = []

        if rgx_task == 1:
            head = r'^\S+\s+\S+\s+\d+\s+\d+\s+'
            patterns = [
                re.compile(r'^10-15\b'),
                re.compile(r'^10-15\s+10:18:51\b'),
                re.compile(r'^\S+\s+\d{2}:\d{2}:51\b'),
                re.compile(head + r'[IDVEFAW]\s+lowmemorykiller\s*:'),
                re.compile(r'^\S+\s+10:18:51\.\d+\s+221\s+'),
                re.compile(head + r'E\s'),
                re.compile(head + r'W\s+PackageManager\s*:'),
                re.compile(head + r'D\s+[^:]*ExoPlayer[^:]*:'),
                re.compile(head + r'[EW]\s+.*\b[\w$-]+\.java:'),
                re.compile(head + r'[IDVEFAW]\s+[^:]+:\s.*\bThread\b'),
            ]
            counts = [0] * len(patterns)

            for line in lines:
                stripped = line.strip()
                for i, p in enumerate(patterns):
                    if p.search(stripped):
                        counts[i] += 1

            output_lines = [str(c) for c in counts]

        elif rgx_task == 2:
            java_file_pattern = re.compile(r'([\w$-]+\.java)(?::\d+)?')
            in_error = False  
            for line in lines:
                stripped = line.strip()
                m = log_pattern.match(stripped)
                if m:
                    level = m.group(5)
                    message = m.group(7) or ''
                    in_error = (level == 'E')
                    if in_error:
                        output_lines.extend(java_file_pattern.findall(message))
                elif in_error:
                    output_lines.extend(java_file_pattern.findall(stripped))

        elif rgx_task == 3:
            seen_pids = []
            seen = set()
            for line in lines:
                m = log_pattern.match(line.strip())
                if m:
                    pid = m.group(3)
                    if pid not in seen:
                        seen.add(pid)
                        seen_pids.append(pid)
            output_lines = seen_pids

        elif rgx_task == 4:
            error_counts = {}
            for line in lines:
                m = log_pattern.match(line.strip())
                if m and m.group(5) == 'E':
                    pid = m.group(3)
                    error_counts[pid] = error_counts.get(pid, 0) + 1
            if error_counts:
                max_pid = max(error_counts, key=error_counts.get)
                max_count = error_counts[max_pid]
                output_lines = [f"PID={max_pid} ({max_count} errors)"]
            else:
                output_lines = ["PID=0 (0 errors)"]

        elif rgx_task == 5:
            main_thread_errors = 0
            for line in lines:
                m = log_pattern.match(line.strip())
                if m and m.group(5) == 'E' and m.group(3) == m.group(4):
                    main_thread_errors += 1
            output_lines = [str(main_thread_errors)]

        with open(out_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_lines) + "\n")