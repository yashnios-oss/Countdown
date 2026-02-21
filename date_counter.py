import streamlit as st
from datetime import date, datetime, timedelta

st.set_page_config(page_title=“Date Counter”, layout=“centered”)
st.title(“Date Counter and Reminders”)
st.markdown(”—”)

if “reminders” not in st.session_state:
st.session_state.reminders = []

# — Days Between Dates —

st.header(“Days Between Two Dates”)
col1, col2 = st.columns(2)
with col1:
start_date = st.date_input(“Start Date”, value=date.today())
with col2:
end_date = st.date_input(“End Date”, value=date.today() + timedelta(days=30))

diff = (end_date - start_date).days
if diff == 0:
st.success(“Both dates are the same.”)
elif diff > 0:
st.info(str(diff) + “ days between the two dates. (” + str(diff // 7) + “ weeks and “ + str(diff % 7) + “ days)”)
else:
st.warning(“End date is before start date by “ + str(abs(diff)) + “ days.”)

st.markdown(”—”)

# — Countdown —

st.header(“Countdown to a Date”)
target = st.date_input(“Target Date”, value=date.today() + timedelta(days=7))
label = st.text_input(“Event Name”, value=“My Event”)
days_left = (target - date.today()).days

if days_left > 0:
st.success(str(days_left) + “ days until “ + label)
st.progress(min(1.0, 1 - days_left / 365))
elif days_left == 0:
st.balloons()
st.success(“Today is the day for “ + label)
else:
st.error(label + “ was “ + str(abs(days_left)) + “ days ago.”)

st.markdown(”—”)

# — Reminders —

st.header(“Reminders”)

with st.form(“add_reminder”, clear_on_submit=True):
col3, col4 = st.columns(2)
with col3:
r_date = st.date_input(“Date”, value=date.today() + timedelta(days=1))
with col4:
r_time = st.time_input(“Time”)
r_note = st.text_input(“Note”)
add = st.form_submit_button(“Add Reminder”)
if add and r_note:
dt = datetime.combine(r_date, r_time)
st.session_state.reminders.append({“note”: r_note, “dt”: dt.isoformat()})
st.success(“Reminder added!”)

if st.session_state.reminders:
st.subheader(“Your Reminders”)
now = datetime.now()
to_del = []
for i, r in enumerate(st.session_state.reminders):
dt = datetime.fromisoformat(r[“dt”])
secs = int((dt - now).total_seconds())
if secs > 0:
d, h, m = secs // 86400, (secs % 86400) // 3600, (secs % 3600) // 60
time_str = str(d) + “d “ + str(h) + “h “ + str(m) + “m left”
elif secs > -3600:
time_str = “DUE NOW”
else:
time_str = “Past”
ca, cb = st.columns([5, 1])
with ca:
st.write(r[“note”] + “ | “ + dt.strftime(”%b %d %Y %I:%M %p”) + “ | “ + time_str)
with cb:
if st.button(“Del”, key=“d” + str(i)):
to_del.append(i)
for i in reversed(to_del):
st.session_state.reminders.pop(i)
if to_del:
st.rerun()
if st.button(“Clear All”):
st.session_state.reminders = []
st.rerun()
else:
st.info(“No reminders added yet.”)
