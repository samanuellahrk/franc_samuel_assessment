# Task Tracker Application – Refactor Summary

This document outlines the changes and improvements made to the original Task Tracker application.

---

## 1. Data Persistence Improvements

- **Added global `id_counter`:**  
  Previously, task IDs were generated using `max(tasks.keys()) + 1`, which could cause duplicates if tasks were deleted.  
  Now, `id_counter` (a variable in the JSON file) ensures unique, sequential task IDs.

- **Improved `load_tasks()` and `save_tasks()`:**  
  - Added error handling for corrupted JSON files.  
  - Automatically initializes an empty task list if the file is missing or invalid.  
  - Handles file I/O errors gracefully when saving tasks.

---

## 2. Task Addition (`add_task`)

- **Input validation:**  
  - Task title cannot be empty.  
  - Due date must be in `YYYY-MM-DD` format and after today's date.

- **Date handling:**  
  - Used a helper function `validate_date_format()` to validate user input.  
  - Converts `due_date` and `created_date` to ISO format strings for storage.

- **Improved user experience:**  
  - Repeatedly prompts until valid input is provided.  
  - Provides clear error messages for invalid input.

---

## 3. Task Update (`update_task`)

- **Input validation:**  
  - Only updates fields if user provides new input.  
  - Uses `validate_date_format()` to validate the new due date.  
  - Ensures the new due date is after the task's `created_date`.

- **User guidance:**  
  - Displays current field values before asking for updates.  
  - Allows users to leave fields empty to retain current values.

---

## 4. Mark Task Complete (`mark_task_complete`)

- **New feature implemented:**  
  - Allows marking tasks as complete.  
  - Checks if a task is already complete and provides feedback.  
  - Persists the updated status in `tasks.json`.

---

## 5. Task Deletion (`delete_task`)

- **Added confirmation:**  
  - Prompts the user for confirmation before deleting a task.  
  - Prevents accidental deletion of tasks.

---

## 6. Task Viewing

- **Improved `view_all_tasks()`:**  
  - Nicely formatted table with columns for ID, title, due date, and status.  
  - Truncates long titles for readability.

- **Improved `view_task()`:**  
  - Validates that task ID exists.  
  - Displays all task details, including `created_date`.

---

## 7. Security & Validation

- **Date validation centralized:**  
  - `validate_date_format()` ensures consistent date parsing across `add_task` and `update_task`.

- **Input sanitization:**  
  - `strip()` used for all text inputs to remove accidental spaces.

---

## 8. Menu & User Interface

- Added option for marking tasks as complete.  
- Menu input validated to prevent invalid choices.  
- Clear and structured prompts guide the user through each action.

---

## Summary

The refactor enhances:

- **Reliability:** Avoids crashes on corrupted JSON or invalid input.  
- **Data Integrity:** Ensures unique task IDs and valid dates.  
- **User Experience:** Provides clear prompts, error messages, and confirmations.  
- **Functionality:** Adds missing features like marking tasks complete and task deletion confirmation.
