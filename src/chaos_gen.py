import random
import time
from datetime import datetime, timedelta
from faker import Faker

# Initialize the Faker generator
fake = Faker()

# ---------------------------------------------------------
# CONSTANTS: The "Menu" of Bad Things
# ---------------------------------------------------------
WAIT_TYPES = [
    "PAGEIOLATCH_SH",   # Disk is slow
    "LCK_M_IX",         # Blocking/Locking
    "CXPACKET",         # Parallelism (CPU)
    "SOS_SCHEDULER_YIELD", # CPU pressure
    "WRITELOG"          # Transaction Log disk slow
]

QUERY_TEMPLATES = [
    "SELECT * FROM Sales.Orders WHERE OrderDate > '{date}'",
    "SELECT COUNT(*) FROM Production.Products WHERE Cost > {price}",
    "UPDATE HumanResources.Employees SET Salary = Salary * 1.1 WHERE ID = {id}",
    "DELETE FROM Audit.Logs WHERE LogDate < '{date}'",
    "SELECT TOP 10 * FROM Customers c JOIN Orders o ON c.ID = o.CustomerID WHERE c.Region = '{region}'"
]

ERROR_MESSAGES = [
    "Login failed for user 'sa'. Reason: Password did not match that for the login provided.",
    "Transaction (Process ID {pid}) was deadlocked on lock resources with another process and has been chosen as the deadlock victim.",
    "The transaction log for database 'SalesDB' is full due to 'LOG_BACKUP'.",
    "Timeout expired. The timeout period elapsed prior to completion of the operation."
]

# ---------------------------------------------------------
# FUNCTION: Generate a Single "Bad" Event
# ---------------------------------------------------------
def generate_event():
    event_type = random.choice(["QUERY", "QUERY", "QUERY", "ERROR"]) # 75% Queries, 25% Errors
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if event_type == "QUERY":
        # Simulate a slow query
        duration = random.randint(100, 15000) # Between 100ms and 15 seconds
        cpu_time = int(duration * random.uniform(0.5, 0.9)) # CPU is usually a % of duration
        logical_reads = random.randint(1000, 500000) # Heavy disk reads
        wait_type = random.choice(WAIT_TYPES)
        
        # Fill in the blanks in the SQL template
        sql_text = random.choice(QUERY_TEMPLATES).format(
            date=fake.date_this_decade(),
            price=random.randint(10, 1000),
            id=random.randint(1, 10000),
            region=fake.state_abbr()
        )
        
        return {
            "type": "QUERY",
            "timestamp": current_time,
            "duration_ms": duration,
            "cpu_time_ms": cpu_time,
            "logical_reads": logical_reads,
            "wait_type": wait_type,
            "sql_text": sql_text
        }
        
    else:
        # Simulate a critical error
        error_msg = random.choice(ERROR_MESSAGES).format(
            pid=random.randint(50, 150)
        )
        
        return {
            "type": "ERROR",
            "timestamp": current_time,
            "severity": random.choice([16, 17, 19, 20]),
            "message": error_msg
        }

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    print("--- STARTING CHAOS GENERATOR (PREVIEW MODE) ---")
    print("Generating 5 sample events...\n")
    
    for _ in range(5):
        event = generate_event()
        print(event)
        time.sleep(0.5) # Pause slightly for dramatic effect
        
    print("\n--- TEST COMPLETE ---")