## Contributing

[fork]: /fork
[pr]: /compare
[code-of-conduct]: CODE_OF_CONDUCT.md

Hi there! We're thrilled that you'd like to contribute to this project. Your help is essential for keeping it great.

Please note that this project is released with a [Contributor Code of Conduct][code-of-conduct]. By participating in this project you agree to abide by its terms.


## Issues and PRs

If you have suggestions for how this project could be improved, or want to report a bug, open an issue! We'd love all and any contributions. If you have questions, too, we'd love to hear them.

We'd also love PRs. If you're thinking of a large PR, we advise opening up an issue first to talk about it, though! Look at the links below if you're not sure how to open a PR.

## Submitting a pull request

1. [Fork][fork] and clone the repository.
1. Configure and install the dependencies: `npm install`.
1. Make sure the tests pass on your machine: `npm test`, note: these tests also apply the linter, so there's no need to lint separately.
1. Create a new branch: `git checkout -b my-branch-name`.
1. Make your change, add tests, and make sure the tests still pass.
1. Push to your fork and [submit a pull request][pr].
1. Pat your self on the back and wait for your pull request to be reviewed and merged.

Here are a few things you can do that will increase the likelihood of your pull request being accepted:

- Write and update tests.
- Keep your changes as focused as possible. If there are multiple changes you would like to make that are not dependent upon each other, consider submitting them as separate pull requests.
- Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).

Work in Progress pull requests are also welcome to get feedback early on, or if there is something blocked you.
## Setting up the environment
1. We use `poetry` to manage the dependencies and the environment. In a virtual environment install the dependencies using `poetry install`

2. Create a `.env` file in the `reviewturtl` directory and add the following environment variables:
- `OPENAI_API_KEY`: The API key for the OpenAI API.
- `ENVIRONMENT`: The environment you are working in.

## Resources

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [Using Pull Requests](https://help.github.com/articles/about-pull-requests/)
- [GitHub Help](https://help.github.com)

## Writing Signatures, Programmes, and Integrating New Agents

### Writing Signatures

Signatures in ReviewTurtl define the input and output fields for various components. To write a new signature:

1. Create a new class that inherits from `dspy.Signature`.
2. Define input fields using `dspy.InputField()`.
3. Define output fields using `dspy.OutputField()`.
4. Add a docstring to describe the signature's purpose and usage.

Example:
```python
class MyNewSignature(dspy.Signature):
    """
    Description of what this signature does.
    """
    input_field = dspy.InputField(desc="Description of the input")
    output_field = dspy.OutputField(desc="Description of the output")
```

### Writing Programmes

Programmes in ReviewTurtl are modules that use signatures to process data. To write a new programme:

1. Create a new class that inherits from `dspy.Module`.
2. Initialize the class with a signature in the `__init__` method.
3. Implement the `forward` method to define the programme's behavior.

Example:
```python
class MyNewProgramme(dspy.Module):
    def __init__(self, signature):
        super().__init__()
        self.predictor = dspy.TypedPredictor(signature)

    def forward(self, model=None, **kwargs):
        if model:
            with dspy.context(lm=model):
                return self.predictor(**kwargs)
        return self.predictor(**kwargs)
```

### Integrating New Agents with the React Agent

To integrate a new agent with the React agent:

1. Create your new agent class inheriting from `Agent`.
2. Implement the required methods, including `__init__` and `forward`.
3. Add your agent to the `agent_dict` in `reviewturtl/src/agents/utils.py`.
4. Update the `ReactAgent` class in `react_agent.py` to handle your new agent if necessary.

Example of adding a new agent to `agent_dict`:
```python
from .my_new_agent import MyNewAgent

agent_dict = {
    # ... existing agents ...
    "MyNewAgent": {
        "class_name": "MyNewAgent",
        "class_object": MyNewAgent(),
        "description": "Description of what MyNewAgent does",
        "input_variables": ["input1", "input2"],
        "output_variables": ["output"],
    },
}
```

Remember to follow the existing code structure and naming conventions when adding new components to the project.
