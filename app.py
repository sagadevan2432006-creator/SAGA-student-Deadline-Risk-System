import streamlit as st
from datetime import date
from database import create_table, add_task, get_tasks, update_task,delete_task
from risk import calculate_risk
from scheduler import generate_schedule
from streamlit_calendar import calendar
from datetime import date

create_table()

st.set_page_config(
    page_title="SAGA",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 SAGA")
with st.sidebar:
    st.title("🎓 SAGA")
    st.write("Student Deadline & Task Risk System")

    st.divider()

    st.subheader("🛠️ Technologies")
    st.write("• Python")
    st.write("• Streamlit")
    st.write("• SQLite")
    st.write("• Plotly")
    st.write("• Rule-Based AI")

    st.divider()

    st.subheader("📌 Features")
    st.write("• Task Management")
    st.write("• Deadline Alerts")
    st.write("• Risk Analysis")
    st.write("• Smart Scheduling")
    st.write("• Calendar")
    st.write("• Progress Tracking")
st.subheader("Student Deadline & Task Risk System")

st.divider()

st.header("➕ Add New Task")

title = st.text_input("Task Name")

deadline = st.date_input(
    "Deadline",
    min_value=date.today()
)

effort = st.number_input(
    "Estimated Effort (hours)",
    min_value=0.5,
    step=0.5
)

priority = st.selectbox(
    "Priority",
    ["Low", "Medium", "High"]
)

if st.button("Add Task"):
    if title.strip():
        try:
                add_task(
                    title,
                    deadline.isoformat(),
                    effort,
                    priority
                )
                st.success("Task added successfully!")
                st.rerun()
        except ValueError as e:
                st.error(str(e))
        
            
    else:
        st.warning("Please enter a task name.")

st.divider()

st.header("📋 Your Tasks")

tasks = get_tasks()

if tasks:
    for task in tasks:
        st.subheader(task[1])

        st.write(f"Deadline: {task[2]}")
        st.write(f"Effort: {task[3]} hours")
        st.write(f"Priority: {task[4]}")
        st.write(f"Status: {task[6]}")

        risk = calculate_risk(
            task[2],
            task[3],
            task[4],
            task[5]
        )

        st.write(f"Risk Level: {risk}")

        progress = st.slider(
            "Progress (%)",
            0,
            100,
            task[5],
            key=f"progress_{task[0]}"
        )
        if st.button("Update Progress", key=f"update_{task[0]}"):
            update_task(task[0], progress)
            st.success("Progress updated!")
            st.rerun()

        if st.button("Delete Task", key=f"delete_{task[0]}"):
            delete_task(task[0])
            st.rerun()

        st.divider()
else:
    st.info("No tasks added yet.")
    st.divider()

st.header("📊 Workload Overview")

if tasks:
    total_tasks = len(tasks)

    total_effort = sum(task[3] for task in tasks)

    remaining_effort = sum(
        task[3] * (1 - task[5] / 100)
        for task in tasks
    )

    high_risk_tasks = sum(
        calculate_risk(
            task[2],
            task[3],
            task[4],
            task[5]
        ) == "High Risk"
        for task in tasks
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Tasks", total_tasks)

    with col2:
        st.metric("Total Effort", f"{total_effort:.1f} hrs")

    with col3:
        st.metric("Remaining Work", f"{remaining_effort:.1f} hrs")

    st.metric("High Risk Tasks", high_risk_tasks)

    if remaining_effort > 10:
        st.warning(
            "⚠️ Heavy workload detected. "
            "You have more than 10 hours of remaining work."
        )
    else:
        st.success("✅ Your current workload is manageable.")
        st.divider()

st.header("🗓️ Suggested Schedule")

if tasks:
    daily_hours = st.number_input(
        "Available study hours per day",
        min_value=1.0,
        max_value=12.0,
        value=4.0,
        step=1.0
    )

    schedule = generate_schedule(tasks, daily_hours)

    if schedule:
        for item in schedule:
            st.write(
                f"📅 {item['date']} — "
                f"{item['task']} — "
                f"{item['hours']} hours"
            )
    else:
        st.success("✅ No remaining work to schedule.")
else:
    st.info("Add tasks to generate a schedule.")
    st.divider()

st.header("⚠️ Workload Risk by Day")

if tasks:
    daily_hours = st.number_input(
        "Maximum comfortable hours per day",
        min_value=1.0,
        max_value=12.0,
        value=4.0,
        step=1.0,
        key="max_daily_hours"
    )

    schedule = generate_schedule(tasks, daily_hours)

    daily_workload = {}

    for item in schedule:
        day = item["date"]

        if day not in daily_workload:
            daily_workload[day] = 0

        daily_workload[day] += item["hours"]

    if daily_workload:
        for day, hours in daily_workload.items():

            if hours >= daily_hours:
                st.warning(
                    f"⚠️ {day}: {hours:.1f} hours of work scheduled"
                )
            else:
                st.success(
                    f"✅ {day}: {hours:.1f} hours of work scheduled"
                )
    else:
        st.info("No workload to analyze.")
else:
    st.info("Add tasks to analyze workload.")
    st.divider()

st.header("📅 Task Calendar")

if tasks:
    events = []

    for task in tasks:
        events.append({
            "title": task[1],
            "start": task[2],
            "allDay": True
        })

    calendar_options = {
        "initialView": "dayGridMonth",
        "editable": False,
        "selectable": False
    }

    calendar(
        events=events,
        options=calendar_options
    )

else:
    st.info("Add tasks to view them on the calendar.")
    st.divider()

st.header("🚨 Upcoming Deadline Alerts")

if tasks:
    today = date.today()

    for task in tasks:
        deadline_date = date.fromisoformat(task[2])
        days_left = (deadline_date - today).days

        if 0 <= days_left <= 3 and task[5] < 100:
            st.warning(
                f"⚠️ {task[1]} is due in {days_left} day(s)!"
            )

else:
    st.info("Add tasks to see deadline alerts.")
    st.divider()

st.header("📈 Progress Overview")

if tasks:
    total_effort = sum(task[3] for task in tasks)

    completed_effort = sum(
        task[3] * task[5] / 100
        for task in tasks
    )

    if total_effort > 0:
        overall_progress = (completed_effort / total_effort) * 100
    else:
        overall_progress = 0

    st.progress(int(overall_progress))

    st.write(
        f"Overall Progress: {overall_progress:.1f}%"
    )

else:
    st.info("Add tasks to see your overall progress.")
    st.divider()

st.header("📌 Task Status Summary")

if tasks:
    pending = sum(task[6] == "Pending" for task in tasks)
    in_progress = sum(task[6] == "In Progress" for task in tasks)
    completed = sum(task[6] == "Completed" for task in tasks)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Pending", pending)

    with col2:
        st.metric("In Progress", in_progress)

    with col3:
        st.metric("Completed", completed)

else:
    st.info("Add tasks to see the task status summary.")
    st.divider()

st.header("ℹ️ About SAGA")

st.write(
    "SAGA is a Student Deadline & Task Risk Management System "
    "that helps students manage tasks, deadlines, workload, "
    "priorities, progress, and study schedules."
)

st.write(
    "The system analyzes deadline, effort, priority, and progress "
    "to identify task risks and provide useful workload insights."
)
st.divider()

st.header("📌 Task Status Summary")

if tasks:
    pending = sum(task[6] == "Pending" for task in tasks)
    in_progress = sum(task[6] == "In Progress" for task in tasks)
    completed = sum(task[6] == "Completed" for task in tasks)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Pending", pending)

    with col2:
        st.metric("In Progress", in_progress)

    with col3:
        st.metric("Completed", completed)

else:
    st.info("Add tasks to see the task status summary.")
    

