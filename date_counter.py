import streamlit as st
from datetime import date, datetime, timedelta
import time
import json

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(page_title=“📅 Date Counter & Reminders”, layout=“centered”)

st.title(“📅 Date Counter & Reminders”)
st.markdown(”—”)

# ── Session state for reminders ───────────────────────────────────────────────

if “reminders” not in st.session_state:
st.session_state.reminders = []

# ═══════════════════════════════════════════════════════════════════════════════

# SECTION 1 — Days Between Two Dates

# ═══════════════════════════════════════════════════════════════════════════════

st.header(“🔢 Days Between Two Dates”)

col1, col2 = st.columns(2)
with col1:
start_date = st.date_input(“Start Date”, value=date.today(), key=“start”)
with col2:
end_date = st.date_input(“End Date”, value=date.today() + timedelta(days=30), key=“end”)

if start_date and end_date:
delta = end_date - start_date
days = delta.days
weeks = abs(days) // 7
remaining_days = abs(days) % 7

```
if days == 0:
    st.success("✅ Both dates are the same!")
elif days > 0:
    st.info(
        f"⏳ **{days} days** from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}\n\n"
        f"That's **{weeks} week(s)** and **{remaining_days} day(s)**."
    )
else:
    st.warning(
        f"⚠️ End date is before start date by **{abs(days)} days** "
        f"({weeks} week(s) and {remaining_days} day(s))."
    )
```

st.markdown(”—”)

# ═══════════════════════════════════════════════════════════════════════════════

# SECTION 2 — Countdown Timer

# ═══════════════════════════════════════════════════════════════════════════════

st.header(“⏰ Countdown to a Target Date”)

target_date = st.date_input(“Select Target Date”, value=date.today() + timedelta(days=7), key=“target”)
target_label = st.text_input(“Label (optional)”, placeholder=“e.g. My Birthday 🎂”)

today = date.today()
countdown_days = (target_date - today).days

if countdown_days > 0:
label_text = f”**{target_label}**” if target_label else “your target date”
st.success(f”🚀 {countdown_days} days remaining until {label_text}!”)

```
# Visual progress bar (assuming a 365-day window)
progress = max(0, min(1, 1 - countdown_days / 365))
st.progress(progress, text=f"Progress toward {target_date.strftime('%B %d, %Y')}")
```

elif countdown_days == 0:
st.balloons()
st.success(“🎉 Today is the day!”)
else:
st.error(f”⚠️ That date was {abs(countdown_days)} day(s) ago.”)

st.markdown(”—”)

# ═══════════════════════════════════════════════════════════════════════════════

# SECTION 3 — Reminders

# ═══════════════════════════════════════════════════════════════════════════════

st.header(“🔔 Reminders”)

with st.form(“reminder_form”, clear_on_submit=True):
r_col1, r_col2 = st.columns(2)
with r_col1:
reminder_date = st.date_input(“Reminder Date”, value=date.today() + timedelta(days=1))
with r_col2:
reminder_time = st.time_input(“Reminder Time”, value=datetime.now().time().replace(second=0, microsecond=0))
reminder_text = st.text_input(“Reminder Note”, placeholder=“e.g. Submit report 📝”)
submitted = st.form_submit_button(“➕ Add Reminder”)

```
if submitted and reminder_text:
    reminder_dt = datetime.combine(reminder_date, reminder_time)
    st.session_state.reminders.append({
        "text": reminder_text,
        "datetime": reminder_dt.isoformat(),
    })
    st.success(f"Reminder added for {reminder_dt.strftime('%B %d, %Y at %I:%M %p')}!")
```

# Display reminders

if st.session_state.reminders:
st.subheader(“📋 Your Reminders”)
now = datetime.now()

```
sorted_reminders = sorted(
    enumerate(st.session_state.reminders),
    key=lambda x: x[1]["datetime"]
)

to_delete = []

for idx, reminder in sorted_reminders:
    reminder_dt = datetime.fromisoformat(reminder["datetime"])
    diff = reminder_dt - now
    total_seconds = int(diff.total_seconds())

    if total_seconds > 0:
        days_left = diff.days
        hours_left = (total_seconds % 86400) // 3600
        mins_left = (total_seconds % 3600) // 60
        countdown_str = f"⏳ {days_left}d {hours_left}h {mins_left}m remaining"
        status_color = "🟢"
    elif total_seconds > -3600:
        countdown_str = "🔔 DUE NOW / Recently due"
        status_color = "🔴"
    else:
        countdown_str = f"✅ Past ({reminder_dt.strftime('%b %d, %Y')})"
        status_color = "⚫"

    with st.container():
        col_a, col_b = st.columns([5, 1])
        with col_a:
            st.markdown(
                f"{status_color} **{reminder['text']}**  \n"
                f"🗓 {reminder_dt.strftime('%B %d, %Y at %I:%M %p')}  \n"
                f"{countdown_str}"
            )
        with col_b:
            if st.button("🗑", key=f"del_{idx}"):
                to_delete.append(idx)

for idx in reversed(to_delete):
    st.session_state.reminders.pop(idx)
if to_delete:
    st.rerun()

if st.button("🗑 Clear All Reminders"):
    st.session_state.reminders = []
    st.rerun()
```

else:
st.info(“No reminders yet. Add one above!”)

st.markdown(”—”)
st.caption(“Built with ❤️ using Streamlit”)
