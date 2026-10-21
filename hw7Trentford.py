Problem 1

def split_logs(machines):
    """Split machine logs by severity and return per-machine counts."""
    counts = {}
    output_names = {
        "INFO": "info.log",
        "WARNING": "warning.log",
        "ERROR": "error.log",
    }

        with open("info.log", "w") as info_file, \
            open("warning.log", "w") as warning_file, \
            open("error.log", "w") as error_file:
        output_files = {
            "INFO": info_file,
            "WARNING": warning_file,
            "ERROR": error_file,
        }

        for machine, log_name in machines.items():
            counts[machine] = {"INFO": 0, "WARNING": 0, "ERROR": 0}

            with open(log_name, "r") as log_file:
                for raw_line in log_file:
                    line = raw_line.strip()
                    if not line:
                        continue

                    level = None
                    for possible_level in output_names:
                        if f"[{possible_level}]" in line:
                            level = possible_level
                            break

                    if level is not None:
                        output_files[level].write(f"{machine} | {line}\n")
                        counts[machine][level] += 1

    return counts


def print_report(counts, error_file="error.log"):
    """Print the security status report in the required format."""
    print("SECURITY LOG REPORT")
    print("=" * 40)

    totals = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    total_entries = 0

    for machine, machine_counts in counts.items():
        info_count = machine_counts["INFO"]
        warning_count = machine_counts["WARNING"]
        error_count = machine_counts["ERROR"]
        entries = info_count + warning_count + error_count
        total_entries += entries

        for level in totals:
            totals[level] += machine_counts[level]

        if error_count >= 2:
            status = "CRITICAL"
        elif error_count >= 1 or warning_count >= 1:
            status = "NEEDS ATTENTION"
        else:
            status = "OK"

        print(
            f"{machine}: {entries} entries | INFO {info_count} | "
            f"WARNING {warning_count} | ERROR {error_count} | Status: {status}"
        )

    print("-" * 40)
    print(
        f"Total: {total_entries} entries | INFO {totals['INFO']} | "
        f"WARNING {totals['WARNING']} | ERROR {totals['ERROR']}"
    )
    print("Errors (see error.log):")

    with open(error_file, "r") as file:
        for line in file:
            print(f"  {line.rstrip()}")


Problem 2

def load_incidents(csv_file):
    """Return a list of incident dictionaries read from a CSV file."""
    incidents = []

    with open(csv_file, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            incidents.append({
                "id": int(row["id"]),
                "machine": row["machine"],
                "severity": row["severity"],
                "description": row["description"],
            })

    return incidents


def save_summary(incidents, json_file):
    """Save a summary to JSON and return the summary dictionary."""
    summary = {
        "total": len(incidents),
        "by_machine": {},
        "by_severity": {},
        "high_ids": [],
    }

    for incident in incidents:
        machine = incident["machine"]
        severity = incident["severity"]

        summary["by_machine"][machine] = (
            summary["by_machine"].get(machine, 0) + 1
        )
        summary["by_severity"][severity] = (
            summary["by_severity"].get(severity, 0) + 1
        )

        if severity.lower() == "high":
            summary["high_ids"].append(incident["id"])

    with open(json_file, "w") as file:
        json.dump(summary, file, indent=2)

    return summary


def archive(incidents, folder):
    """Pickle all incidents and write one JSON file per machine."""
    os.makedirs(folder, exist_ok=True)

    pickle_path = os.path.join(folder, "incidents.pkl")
    with open(pickle_path, "wb") as file:
        pickle.dump(incidents, file)

    machines = []
    for incident in incidents:
        machine = incident["machine"]
        if machine not in machines:
            machines.append(machine)

    for machine in machines:
        machine_incidents = [
            incident for incident in incidents
            if incident["machine"] == machine
        ]
        json_path = os.path.join(folder, f"{machine}.json")
        with open(json_path, "w") as file:
            json.dump(machine_incidents, file, indent=2)

    return sorted(os.listdir(folder))


def load_archive(folder):
    """Return the incident list stored in folder/incidents.pkl."""
    pickle_path = os.path.join(folder, "incidents.pkl")
    with open(pickle_path, "rb") as file:
        return pickle.load(file)


Problem 3

def organize(folder):
    """Move direct files into logs/, data/, pickles/, and other/."""
    categories = {
        "logs": [],
        "data": [],
        "pickles": [],
        "other": [],
    }
    extensions = {
        ".log": "logs",
        ".csv": "data",
        ".json": "data",
        ".pkl": "pickles",
    }

    for name in sorted(os.listdir(folder)):
        source_path = os.path.join(folder, name)

        
        if not os.path.isfile(source_path):
            continue

        extension = os.path.splitext(name)[1].lower()
        category = extensions.get(extension, "other")
        destination_folder = os.path.join(folder, category)
        os.makedirs(destination_folder, exist_ok=True)

        shutil.move(source_path, os.path.join(destination_folder, name))
        categories[category].append(name)

    for category in categories:
        categories[category].sort()

    return categories


def create_backup(source_dir, backup_root, label):
    """Copy source_dir into backup_root/backup_<label> and return its path."""
    os.makedirs(backup_root, exist_ok=True)
    backup_dir = os.path.join(backup_root, f"backup_{label}")

    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)

    shutil.copytree(source_dir, backup_dir)
    return backup_dir


def verify_backup(source_dir, backup_dir):
    """Check that every source file exists in backup with the same byte size."""
    for root, _, files in os.walk(source_dir):
        for name in files:
            source_path = os.path.join(root, name)
            relative_path = os.path.relpath(source_path, source_dir)
            backup_path = os.path.join(backup_dir, relative_path)

            if not os.path.isfile(backup_path):
                return False

            if os.path.getsize(source_path) != os.path.getsize(backup_path):
                return False

    return True


def cleanup_old_backups(backup_root, keep):
    """Keep the newest `keep` backup folders and delete older ones."""
    if not os.path.isdir(backup_root):
        return []

    backup_names = sorted(
        name for name in os.listdir(backup_root)
        if name.startswith("backup_")
        and os.path.isdir(os.path.join(backup_root, name))
    )

    if keep < 0:
        keep = 0

    to_delete = backup_names[:-keep] if keep else backup_names
    for name in to_delete:
        path = os.path.join(backup_root, name)
        print(f"Deleting old backup: {path}")
        shutil.rmtree(path)

    return sorted(to_delete)



