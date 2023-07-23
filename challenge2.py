#sample solution 43% overall score
def assign_tasks(factor, arrival, bonus, reward, duration, time_bonus):
    """Assign tasks to processors. Sample strategy."""

    def intersects(a1, b1, a2, b2):
        return max(a1, a2) < min(b1, b2)

    num_tasks = len(factor)
    num_processors = len(factor[0])
    schedule = [(-1, -1)] * num_tasks
    first_t_safe = [0] * num_processors
    for i in range(num_tasks):
        for j in range(num_processors):
            schedule[i] = (j, arrival[i])
            for k in range(i):
                if schedule[k][0] != j or not intersects(
                    arrival[i], arrival[i] + duration[i], arrival[k], arrival[k] + duration[k]
                ):
                    schedule[i] = (j, arrival[i])
                if schedule[k][0] == j and intersects(
                    arrival[i],
                    arrival[i] + duration[i],
                    schedule[k][1],
                    schedule[k][1] + duration[k],
                ):
                    schedule[i] = (-1, -1)
                    break
            if schedule[i][0] == j:
                break
        if schedule[i][0] >= 0:
            first_t_safe[schedule[i][0]] = max(
                arrival[i] + duration[i], first_t_safe[schedule[i][0]]
            )
            continue
        (m, first_t) = min(enumerate(first_t_safe), key=lambda x: x[1])
        first_t = max(first_t, arrival[i])
        schedule[i] = (m, first_t)
        first_t_safe[m] = first_t + duration[i]
    return schedule
