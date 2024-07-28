import pandas as pd
import dspy
from reviewturtl.settings import get_4o_token_model


class TurtlBaseOptimizer:
    def __init__(self, optimizer_name: str):
        self.optimizer_name = optimizer_name

    def load_prompt_model(self, model):
        if model is None:
            model = get_4o_token_model()
        self.prompt_model = model

        return self.prompt_model

    def load_task_model(self, model):
        if model is None:
            model = get_4o_token_model()
        self.task_model = model
        return self.task_model

    def load_trainset(
        self,
        csv_path: str,
        use_columns: list[str],
        input_columns: list[str],
        output_columns: list[str],
    ):
        # by default, read all columns
        if use_columns is None:
            trainset_csv = pd.read_csv(csv_path)
            use_columns = trainset_csv.columns
        else:
            # if use columns is specified, read only those columns
            trainset_csv = pd.read_csv(csv_path, usecols=use_columns)
        # Convert the dataframe to a list of dspy.Example objects
        trainset = [
            # Dspy Example object
            dspy.Example(**{col: row[col] for col in use_columns}).with_inputs(
                *input_columns
            )
            for _, row in trainset_csv.iterrows()
        ]
        return trainset

    def load_optimizer(self):
        raise NotImplementedError("Subclass must implement this method")

    def generate_training_data(self):
        pass

    def test_student_model(self):
        pass

    def optimize(self):
        raise NotImplementedError("Subclass must implement this method")
