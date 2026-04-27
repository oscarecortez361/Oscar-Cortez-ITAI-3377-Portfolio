import collections
import datetime as dt
import random  # TODO: replace with real MQTT values
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Keep only the last 100 samples
MAX_LEN = 100
times = collections.deque(maxlen=MAX_LEN)
temps = collections.deque(maxlen=MAX_LEN)
hums  = collections.deque(maxlen=MAX_LEN)

# Create the figure and axes
fig, ax = plt.subplots()
fig.canvas.manager.set_window_title("Temperature and Humidity")

# Two line objects: blue for Temperature, orange for Humidity
line_temp, = ax.plot([], [], color="tab:blue", label="Temperature")
line_hum,  = ax.plot([], [], color="tab:orange", label="Humidity")

ax.set_xlabel("Time")
ax.set_ylabel("Value")
ax.legend(loc="upper right")  # or "upper left"

def get_new_data():
    """
    TEMP: right now this just makes fake values.
    Replace this with your latest MQTT temperature and humidity.
    """
    temp = 20 + random.random() * 5      # 20–25
    hum  = 30 + random.random() * 20     # 30–50
    return temp, hum

def update(frame):
    # Current time as label (x-axis)
    now = dt.datetime.now().strftime("%H:%M:%S")

    # Get new data point
    temp, hum = get_new_data()

    # Append to deques (older than 100 are auto-removed)
    times.append(now)
    temps.append(temp)
    hums.append(hum)

    # Use index 0..N-1 as x, values as y
    x_vals = range(len(times))
    line_temp.set_data(x_vals, temps)
    line_hum.set_data(x_vals, hums)

    # X limit: full range we currently have
    ax.set_xlim(0, max(1, len(times) - 1))

    # Y limit: enough to show 20–25 and 30–50
    ax.set_ylim(15, 55)

    # Show a few readable time labels
    if len(times) > 1:
        step = max(1, len(times) // 5)
        ax.set_xticks(range(0, len(times), step))
        ax.set_xticklabels(list(times)[::step], rotation=45, ha="right")

    return line_temp, line_hum

# Call update() every 1000 ms (1 second)
ani = animation.FuncAnimation(fig, update, interval=1000, blit=False)

plt.tight_layout()
plt.show()
