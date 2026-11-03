import time


def read_tasks():
    try:
        with open("task.txt", "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []


def main():
    while True:
        choice = input(
            "\n(S)Start a task\n(C)Create a new task\n(R)Report\n(RE)Reset\n(Q)Quit\n: ").strip().upper()

        if choice == "Q":
            break
        elif choice == "S":
            timer()
        elif choice == "C":
            create_task()
        elif choice == "R":
            report()
        elif choice == "RE":
            reset()
        else:
            print("Please enter a valid option.")


def create_task():
    new_task = input("New task name: ").strip()
    if not new_task or "," in new_task:
        print("Task name can't be empty or contain a comma.")
        return
    if new_task in read_tasks():
        print("That task already exists.")
        return
    with open("task.txt", "a") as file:
        file.write(f"{new_task}\n")


def timer():
    tasks = read_tasks()
    while True:
        task = input("TASK (press 'M' for Menu): ").strip()
        if task.upper() == "M":
            return
        if not task or "," in task:
            print("Task name can't be empty or contain a comma.")
            continue
        if task not in tasks:
            tasks.append(task)
            with open("task.txt", "a") as file:
                file.write(f"{task}\n")

        start = time.time()
        input("Press Enter whenever the task is done...")
        task_time = time.time() - start

        print(f"task: {task}\ntime taken: {minute_converter(task_time)}")

        with open("log.txt", "a") as file:
            file.write(f"{task},{round(task_time, 1)}\n")


def report():
    try:
        with open("log.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    totals = {}
    counts = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        task, seconds = line.rsplit(",", 1)
        totals[task] = totals.get(task, 0) + float(seconds)
        counts[task] = counts.get(task, 0) + 1

    if not totals:
        print("No sessions logged yet.")
        return

    print()
    for task, total in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"{task}: {minute_converter(total)} ({counts[task]} sessions)")


def reset():
    if input("Type YES to erase the whole log: ").strip() == "YES":
        with open("log.txt", "w") as file:
            file.write("")
        print("Log cleared.")
    else:
        print("Cancelled.")


def minute_converter(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"


if __name__ == "__main__":
    main()