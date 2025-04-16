import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

# Load data from the CSV file
df = pd.read_csv("osc_data.csv")

# Extract the necessary columns
eyes_y = df["/avatar/parameters/EyesY"]
left_eye_x = df["/avatar/parameters/RightEyeX"]

# Create the figure and axes
fig, ax = plt.subplots()
line, = ax.plot([], [], marker='o')  # 'o' for circle markers

# Set axis limits
ax.set_xlim(min(left_eye_x), max(left_eye_x))
ax.set_ylim(min(eyes_y), max(eyes_y))

# Set labels
ax.set_xlabel("LeftEyeX")
ax.set_ylabel("EyesY")
ax.set_title("EyesY vs LeftEyeX Animation")

# Animation function
def animate(i):
    x = left_eye_x[:i+1]
    y = eyes_y[:i+1]
    line.set_data(x, y)
    return line,

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=len(df), interval=200, blit=True)

# Display the animation
plt.show()