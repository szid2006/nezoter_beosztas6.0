from flask import Blueprint, render_template, request
from datetime import datetime
from .auth import login_required
from .models import Worker, Shift
from .scheduler import generate_schedule

main = Blueprint("main", __name__)

WORKERS = []
SHIFTS = []

ROLES = {
    "Nézőtér beülős": 2,
    "Nézőtér csak csipog": 2,
    "Jolly joker": 1,
    "Ruhatár bal": 2,
    "Ruhatár jobb": 1,
    "Ruhatár erkély": 1
}


@main.route("/shifts", methods=["GET", "POST"])
@login_required
def shifts():
    if request.method == "POST":
        show = request.form["show"]
        dt = datetime.fromisoformat(request.form["datetime"])

        required = {}
        for role in ROLES:
            count = int(request.form.get(role, 0))
            if count > 0:
                required[role] = count

        SHIFTS.append(Shift(show, dt, required))

    return render_template("shifts.html", roles=ROLES, shifts=SHIFTS)


@main.route("/workers", methods=["GET", "POST"])
@login_required
def workers():
    if request.method == "POST":
        name = request.form["name"]
        preferred = request.form.get("preferred", "").split(",")
        is_ek = "is_ek" in request.form

        WORKERS.append(
            Worker(name, [], preferred, is_ek)
        )

    return render_template("workers.html", workers=WORKERS)


@main.route("/generate")
@login_required
def generate():
    schedule = generate_schedule(WORKERS, SHIFTS)
    return render_template("result.html", schedule=schedule)
