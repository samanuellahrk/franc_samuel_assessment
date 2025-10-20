#!/usr/bin/env python3
"""
Task Tracker Application

A simple console application for tracking tasks.
"""
import json
import os
from datetime import datetime
import time

# Global variables
TASKS_FILE = "tasks.json"
tasks = {}
id_counter = 1  # Initialize a global counter for task IDs


# Bug: Silent failure on corrupted JSON, doesn't initialize 'tasks'
# Fix: 
# - Initialize 'tasks' and 'id_counter' if loading fails
# - Initializes empty task file if it doesn't exist
def load_tasks():
    """Load tasks from the JSON file."""
    global tasks, id_counter
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as f:
                data = json.load(f)
                tasks = data.get("tasks", {})
                id_counter = data.get("id_counter", 1)
        except json.JSONDecodeError:
            # Bug: Silent failure on corrupted JSON, doesn't initialize 'tasks'
            print("Warning: Tasks file is corrupted.")
            # added empty task init if file is corrupted
            tasks = {}
            id_counter = 1
            save_tasks()
    else:
        # Create an empty JSON file if it doesn't exist
        tasks = {}
        id_counter = 1
        save_tasks()

# Bug: No error handling for file operations
# Fix: Added try-except block to handle IOError
def save_tasks():
    """Save tasks to the JSON file."""
    try:
        with open(TASKS_FILE, "w") as f:
            json.dump({"tasks": tasks, "id_counter": id_counter}, f, indent=4)

    # added error handling for file operations
    except IOError as e:
        print(f"Error saving tasks: {e}")

# Bug: This doesn't guarantee uniqueness if tasks are deleted
# Fix: Use a global counter that increments with each new task, ensuring uniqueness
def generate_task_id():
    """Generate a new unique task ID using id_counter."""
    global id_counter
    task_id = id_counter
    id_counter += 1
    save_tasks()  # Persist the updated id_counter
    return task_id

# Bug: 
# - Missing validation for empty title
# - No validation or error handling for date format
# - No validation that the date is in the future
# - Missing created_date field required by specs
# Fix:
# - Added a loop to ensure the title is not empty
# - Added date format validation using `validate_date_format()`
# - Added check to ensure due date is after today's date
# - Added `created_date` field when storing the task
def add_task():
    """Add a new task."""
    print("\n=== Add New Task ===")

    created_date = datetime.now().date() # current date as created date
    
    while True:
        title = input("Enter task title: ").strip() # to remove trailing/leading spaces
        
        if title:
            break
        print("Title cannot be empty. Please enter a valid title.")
    
    description = input("Enter task description: ")
    
    while True:
        due_date_str = input("Enter due date (YYYY-MM-DD): ").strip()
        due_date = validate_date_format(due_date_str)
        if not due_date:
            print("Invalid date format. Please use YYYY-MM-DD.")
            continue
        if due_date <= created_date:
            print("Due date must be after today's date.")
            continue
        break

    task_id = str(generate_task_id())
    tasks[task_id] = {
        "title": title,
        "description": description,
        "due_date": due_date.isoformat(),  # Convert to string
        "created_date": created_date.isoformat(),  # Convert to string
        "status": "incomplete",
    }
    
    save_tasks()
    print(f"Task {task_id} added successfully!")

# Bug: This doesn't format output nicely with proper spacing
# Fix: Adjusted spacing and added truncation for long titles
def view_all_tasks():
    """View all tasks."""
    print("\n=== All Tasks ===")
    
    if not tasks:
        print("No tasks found.")
        return
    
    print(f"{'ID':<5} {'Title':<20} {'Due Date':<12} {'Status':<10}")
    print("-" * 50)
    for task_id, task in tasks.items():
        title = task['title']
        if len(title) > 15:
            display_title = title[:12] + '...'
        else:
            display_title = title
        print(f"{task_id:<5} {display_title:<20} {task['due_date']:<12} {task['status']:<10}")    
    print("-" * 50)

# Bug: Missing validation for non-existent task IDs
# Fix: Added a loop to ensure the task ID exists before proceeding
def view_task():
    """View details of a specific task."""
    print("\n=== View Task ===")
    
    while True:
        task_id = input("Enter task ID: ")

        if task_id in tasks:
            break
        print(f"Task {task_id} not found.")
            
    
    task = tasks[task_id]
    print(f"ID: {task_id}")
    print(f"Title: {task['title']}")
    print(f"Description: {task['description']}")
    print(f"Created Date: {task['created_date']}")
    print(f"Due Date: {task['due_date']}")
    print(f"Status: {task['status']}")

# Bug: 
# - Missing validation for non-existent task IDs
# - No validation on due date format
# - No validation of date format
# Fix:
# - Added a loop to ensure task ID exists before updating
# - Added date validation using `validate_date_format()`
# - Added check to ensure updated due date is after the task's created date
def update_task():
    """Update an existing task."""
    print("\n=== Update Task ===")
    
    while True:
        task_id = input("Enter task ID: ")

        if task_id in tasks:
            break
        print(f"Task {task_id} not found.")
    
    task = tasks[task_id]
    
    print("Leave field empty to keep current value.")
    print(f"Current Title: {task['title']}")
    new_title = input("New Title: ")
    
    print(f"Current Description: {task['description']}")
    new_description = input("New Description: ")
    
    print(f"Current Due Date: {task['due_date']}")
    while True:
        new_due_date_str = input("New Due Date (YYYY-MM-DD): ").strip()
        if not new_due_date_str:
            break  # Keep current due date
        
        new_due_date = validate_date_format(new_due_date_str)
        if not new_due_date:
            print("Invalid date format. Please use YYYY-MM-DD.")
            continue
        
        created_date = datetime.strptime(task['created_date'], "%Y-%m-%d").date()
        if new_due_date <= created_date:
            print("Due date must be after the task's created date.")
            continue
        
        task['due_date'] = new_due_date.isoformat()
        break
        
    # Update task with new values, keeping old values if input is empty
    if new_title:
        task['title'] = new_title
    if new_description:
        task['description'] = new_description
    if new_due_date:
        task['due_date'] = new_due_date
    
    save_tasks()
    print(f"Task {task_id} updated successfully!")

# Bug: Missing implementation of mark_task_complete function (FR1.7)
# Fix: Implemented the function to mark a task as complete
def mark_task_complete():
    """Mark a task as complete."""
    print("\n=== Mark Task as Complete ===")
    
    while True:
        task_id = input("Enter task ID: ")

        if task_id in tasks:
            break
        print(f"Task {task_id} not found.")
    
    task = tasks[task_id]
    if task['status'] == 'complete':
        print(f"Task {task_id} is already marked as complete.")
    else:
        task['status'] = 'complete'
        save_tasks()
        print(f"Task {task_id} marked as complete!")

# Bug: Missing confirmation before deletion
# Fix: Added a confirmation prompt before deleting a task
def delete_task():
    """Delete a task."""
    print("\n=== Delete Task ===")
    
    task_id = input("Enter task ID: ")
    
    if task_id not in tasks:
        print(f"Task {task_id} not found.")
        return
    
    choice = input(f"Are you sure you want to delete task {task_id}? (y/n): ").strip().lower()
    
    if choice == 'y':
        del tasks[task_id]
        save_tasks()
        print(f"Task {task_id} deleted successfully!")
    else:
        print("Deletion cancelled.")
    

def display_menu():
    """Display the main menu."""
    print("\n=== Task Tracker ===")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Task")
    print("4. Update Task")
    print("5. Mark Task as Complete")
    print("6. Delete Task")
    print("7. Exit")

# Added date validation helper function
def validate_date_format(date_str):
    """Return a date object if valid, else None."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None
# Bug: No validation on choice input
# Fix: Added validation to ensure choice is within valid range
def main():
    """Main application function."""
    load_tasks()
    
    while True:
        display_menu()
        
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            add_task()
        elif choice == "2":
            view_all_tasks()
        elif choice == "3":
            view_task()
        elif choice == "4":
            update_task()
        elif choice == "5":
            mark_task_complete()
        elif choice == "6":
            delete_task()
        elif choice == "7":
            print("Exiting Task Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 