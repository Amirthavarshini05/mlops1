import matplotlib.pyplot as plt

# 10 sample data points for each DORA metric

days = [
    "Day 1", "Day 2", "Day 3", "Day 4", "Day 5",
    "Day 6", "Day 7", "Day 8", "Day 9", "Day 10"
]

# Deployment Frequency - deployments per day
deployment_frequency = [2, 3, 2, 4, 3, 2, 5, 3, 4, 3]

# Lead Time for Changes - hours
lead_time = [4, 3, 5, 2, 4, 3, 6, 2, 3, 4]

# Change Failure Rate - percentage
cfr = [10, 20, 10, 15, 20, 10, 25, 15, 10, 20]

# MTTR - hours
mttr = [3, 2, 4, 3, 5, 2, 4, 3, 2, 4]


# Calculate averages
avg_deployment_frequency = sum(deployment_frequency) / len(deployment_frequency)
avg_lead_time = sum(lead_time) / len(lead_time)
avg_cfr = sum(cfr) / len(cfr)
avg_mttr = sum(mttr) / len(mttr)


# Print calculated results
print("DORA Metrics")
print("--------------------------------")
print(f"Average Deployment Frequency : {avg_deployment_frequency:.2f} deployments/day")
print(f"Average Lead Time            : {avg_lead_time:.2f} hours")
print(f"Average Change Failure Rate  : {avg_cfr:.2f}%")
print(f"Average MTTR                 : {avg_mttr:.2f} hours")


# Create dashboard
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Chart 1 - Deployment Frequency
axes[0, 0].plot(days, deployment_frequency, marker="o")
axes[0, 0].set_title("Deployment Frequency")
axes[0, 0].set_xlabel("Day")
axes[0, 0].set_ylabel("Deployments per Day")
axes[0, 0].tick_params(axis="x", rotation=45)
axes[0, 0].grid(True)

# Chart 2 - Lead Time
axes[0, 1].plot(days, lead_time, marker="o")
axes[0, 1].set_title("Lead Time for Changes")
axes[0, 1].set_xlabel("Day")
axes[0, 1].set_ylabel("Hours")
axes[0, 1].tick_params(axis="x", rotation=45)
axes[0, 1].grid(True)

# Chart 3 - Change Failure Rate
axes[1, 0].plot(days, cfr, marker="o")
axes[1, 0].set_title("Change Failure Rate")
axes[1, 0].set_xlabel("Day")
axes[1, 0].set_ylabel("Failure Rate (%)")
axes[1, 0].tick_params(axis="x", rotation=45)
axes[1, 0].grid(True)

# Chart 4 - MTTR
axes[1, 1].plot(days, mttr, marker="o")
axes[1, 1].set_title("Mean Time to Recovery")
axes[1, 1].set_xlabel("Day")
axes[1, 1].set_ylabel("Hours")
axes[1, 1].tick_params(axis="x", rotation=45)
axes[1, 1].grid(True)

# Main dashboard title
fig.suptitle("DORA Metrics Dashboard", fontsize=18)

# Adjust spacing
plt.tight_layout()

# Display dashboard
plt.show()