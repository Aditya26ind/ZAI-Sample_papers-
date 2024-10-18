# app/core/tasks.py
from app.services.gemini_service import GeminiService

class TaskManager:
    def __init__(self):
        self.tasks = {}

    async def process_pdf_task(self, task_id, file):
        gemini_service = GeminiService()
        result = await gemini_service.extract_pdf(file)
        self.tasks[task_id] = result

    def get_task_status(self, task_id):
        return self.tasks.get(task_id, "Task not found")

task_manager = TaskManager()
