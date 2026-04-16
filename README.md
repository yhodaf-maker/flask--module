# flask--module

# My First Flask API

Simple Flask API for managing tasks.

## What It Does

* Get all tasks
* Get task by ID
* Create new task
* Update task
* Delete task

## Run The App

```bash
python app.py
```

Runs on:

```
http://127.0.0.1:5000
```

## Endpoints

### GET /tasks

Returns all tasks

### GET /tasks/<task_id>

Returns one task

### POST /tasks

Create new task

Example:

```json
{
  "title": "Buy milk"
}
```

### PUT /tasks/<task_id>

Update task

Example:

```json
{
  "title": "New title",
  "completed": true
}
```

### DELETE /tasks/<task_id>

Delete task

## Notes

* Data is stored in memory
* Restarting server resets tasks

