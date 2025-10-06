import random
import time

# --- Simulated Logs ---
logs = [
    "INFO: Service started successfully",
    "INFO: Processing request",
    "ERROR: Connection timeout",
    "INFO: Request completed",
    "ERROR: Failed to fetch data",
]

# --- Simple Environment / Auto-Heal ---
class LogEnvironment:
    def __init__(self, logs):
        self.logs = logs
        self.errors_fixed = 0

    def scan_logs(self):
        """Scan logs and detect errors."""
        error_lines = [line for line in self.logs if "ERROR" in line]
        return error_lines

    def auto_heal(self):
        """Simulate a container restart."""
        print("⚡ Auto-Heal triggered: restarting container...")
        time.sleep(1)  # Simulate recovery delay
        fixed_errors = self.scan_logs()
        self.errors_fixed += len(fixed_errors)
        # Remove fixed errors from logs
        self.logs = [line for line in self.logs if "ERROR" not in line]
        print(f"✅ Fixed {len(fixed_errors)} errors.")
        return len(fixed_errors)

# --- Simple RL Policy ---
class RLAgent:
    def __init__(self):
        self.total_reward = 0

    def decide(self, errors_detected):
        """Policy: trigger auto-heal if any errors detected."""
        if errors_detected:
            return "heal"
        return "wait"

    def update_reward(self, fixed_errors):
        """Give positive reward for fixing errors."""
        reward = fixed_errors * 10
        self.total_reward += reward
        print(f"🎯 Reward: {reward} | Total Reward: {self.total_reward}")

# --- Main Loop ---
env = LogEnvironment(logs)
agent = RLAgent()

for step in range(5):
    print(f"\n--- Step {step + 1} ---")
    errors = env.scan_logs()
    print(f"Detected errors: {errors}")

    action = agent.decide(errors)
    if action == "heal":
        fixed = env.auto_heal()
        agent.update_reward(fixed)
    else:
        print("No action needed.")

    # Simulate new log events
    if random.random() < 0.5:
        env.logs.append("ERROR: Random failure occurred")
    else:
        env.logs.append("INFO: Routine operation completed")
