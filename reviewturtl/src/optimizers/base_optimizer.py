class TurtlBaseOptimizer:
    def __init__(self, optimizer_name: str):
        self.optimizer_name = optimizer_name

    def load_prompt_model(self):
        pass

    def load_task_model(self):
        pass

    def load_training_data(self):
        pass

    def generate_training_data(self):
        pass

    def test_student_model(self):
        pass

    def optimize(self):
        pass
