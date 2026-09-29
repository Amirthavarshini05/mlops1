import matplotlib.pyplot as plt

metrics = [
    "Deployment\nFrequency",
    "Lead Time",
    "Change Failure\nRate",
    "Recovery Time"
]

values = [2, 2.7, 20, 2.5]

plt.figure(figsize=(10, 6))
plt.bar(metrics, values)

plt.title("DORA Metrics")
plt.ylabel("Metric Value")
plt.xlabel("DORA Metrics")

plt.tight_layout()
plt.show()