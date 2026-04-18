from flask import Flask, render_template, redirect, request

app = Flask(__name__)

candidates = {
        "APP-1024": {
            "name": "Harshit Jain",
            "role": "LLM engineer",
            "application_id": "APP-1024",
            "status": "Verified",
            "metric_pills": [
                {"label": "Skill", "value": 92, "color": "blue"},
                {"label": "Health", "value": 95, "color": "green"}
            ],
            "skills": ["MySQL","Python", "LLM"],
            "phone":"+91 9521426624",
            "email": "harshit@jain.com"
        },
    }

conflicts = [
    {
        "name": "Suyash Srivastav",
        "role": "Legal Consuel",
        "reason": "Email Conflict",
        "confidence": 95,
        "count": 1,
        "phone":"+91 9686112474",
        "metric_pills": [
                {"label": "Skill", "value": 85, "color": "blue"},
                {"label": "Health", "value": 90, "color": "green"}
            ],
        "status_pill": {"text": "Verified"},
        "skills": ["MySQL","Python"],
        "sources": [
            {
                "name": "LinkedIn",
                "updated": "Updated 5 hours ago",
                "fields": [
                    {"label": "Email", "key": "email", "value": "suyash.s.analytics@gmail.com", "conflict": True, "selected": True}
                ]
            },
            {
                "name": "Naukri",
                "updated": "Updated 2 months ago",
                "fields": [
                    {"label": "Email", "key": "email", "value": "suyash@hotmail.com", "conflict": True, "selected": False}
                ]
            }
        ]
    },
    {
        "name": "Shivam Somani",
        "role": "Operations lead",
        "reason": "email Conflict",
        "confidence": 94,
        "count": 1,
        "phone":"+91 9686112474",
        "metric_pills": [
                {"label": "Skill", "value": 85, "color": "blue"},
                {"label": "Health", "value": 90, "color": "green"}
            ],
        "status_pill": {"text": "Verified"},
        "skills": ["MySQL","Python","SCM"],
        "sources": [
            {
                "name": "LinkedIn",
                "updated": "Updated 5 hours ago",
                "fields": [
                    {"label": "Email", "key": "email", "value": "Shivam.s.analytics@gmail.com", "conflict": True, "selected": True}
                ]
            },
            {
                "name": "Referal",
                "updated": "Updated 2 months ago",
                "fields": [
                    {"label": "Email", "key": "email", "value": "Shivam@hotmail.com", "conflict": True, "selected": False}
                ]
            }
        ]
    },

    {
        "name": "A Ravichandra",
        "reason": "Phone & Name Conflict",
        "role": "CEO",
        "skills": ["MySQL","Python"],
        "metric_pills": [
                {"label": "Skill", "value": 73, "color": "blue"},
                {"label": "Health", "value": 70, "color": "green"}
            ],
        "status_pill": {"text": "Verified"},
        "confidence": 90,
        "email": "ravi@bits.com",
        "count": 2,
        "sources": [
            {
                "name": "Linkedin",
                "updated": "Updated 3 months ago",
                "fields": [
                    {"label": "Name", "key": "name", "value": "A Ravichandra", "selected": True},
                    {"label": "Phone", "key": "phone", "value": "+91 7447351528", "selected": False}
                ]
            },
            {
                "name": "Referral",
                "updated": "Updated 1 week ago",
                "fields": [
                    {"label": "Name", "key": "name", "value": "Ravichandra A", "selected": False},
                    {"label": "Phone", "key": "phone", "value": "+91 9739760421", "selected": True}
                ]
            }
        ]
    }
]

# ---------------- DASHBOARD (NEW UI) ----------------
@app.route("/")
def dashboard():
    return render_template("home.html",conflicts=conflicts,)

# ---------------- CANDIDATE PROFILES ----------------
@app.route("/candidates")
def candidates_page():
    return render_template("candidates.html", candidates=candidates)

# ---------------- REVIEW QUEUE ----------------
@app.route("/review")
def review():
    return render_template("review.html",conflicts=conflicts)
# ---------------- Archive ----------------
@app.route("/archive")
def archive():
    return render_template("archive.html")

# ---------------- APPROVE / REJECT ----------------
@app.route("/confirm_merge", methods=["POST"])
def confirm_merge():
    global conflicts, candidates
    selected_data = {}
    for key, value in request.form.items():
        if key.startswith("field_"):
            logical_key = key.replace("field_", "")
            selected_data[logical_key] = value
    conflict_index = int(request.form.get("conflict_index"))
    merged_conflict = conflicts.pop(conflict_index)
    new_id = f"APP-{1024 + len(candidates)}"
    new_candidate = {
        **merged_conflict,
        "application_id": new_id,
        "status": "Merged"
    }
    for k, v in selected_data.items():
        new_candidate[k] = v
    candidates[new_id] = new_candidate

    return redirect("/candidates")

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")