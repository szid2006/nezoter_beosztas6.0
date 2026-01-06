def is_available(worker, shift):
    for start, end in worker.unavailable:
        if start <= shift.datetime <= end:
            return False
    return True


def ek_allowed(worker, role, ek_used):
    if not worker.is_ek:
        return True
    if ek_used:
        return False
    if role == "Jolly joker":
        return False
    return True


def preference_bonus(worker, shift, role):
    if shift.show_name in worker.preferred_shows:
        if role == "Nézőtér beülős":
            return -5
    return 0


def score(worker, shift, role):
    return (
        worker.assign_count * 2
        + worker.role_history.count(role)
        + (5 if worker.is_ek else 0)
        + preference_bonus(worker, shift, role)
    )


def already_worked_today(worker, shift, schedule):
    for s in schedule:
        if s.datetime.date() == shift.datetime.date():
            for names in s.assigned.values():
                if worker.name in names:
                    return True
    return False


def generate_schedule(workers, shifts):
    schedule = []

    for shift in shifts:
        ek_used = False

        for role, count in shift.required_roles.items():
            for _ in range(count):
                candidates = [
                    w for w in workers
                    if is_available(w, shift)
                    and not already_worked_today(w, shift, schedule)
                    and ek_allowed(w, role, ek_used)
                ]

                if not candidates:
                    continue

                chosen = min(candidates, key=lambda w: score(w, shift, role))

                shift.assigned.setdefault(role, []).append(chosen.name)
                chosen.assign_count += 1
                chosen.role_history.append(role)

                if chosen.is_ek:
                    ek_used = True

        schedule.append(shift)

    return schedule
