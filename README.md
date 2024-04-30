# LicencIAdo
## Set up
You will need [anaconda](https://www.anaconda.com/download/success) for this project.

1. Create an env for the project: `conda create --name licenciado --file requirements.txt`
2. Activate the env: `conda activate licenciado`
3. Setup OpenAI and Anthropic API keys:
    - `conda env config vars set OPENAI_API_KEY=<your_key>`
    - `conda env config vars set ANTHROPIC_API_KEY=<your_key>`
4. Restart the env:
    - `conda deactivate`
    - `conda activate licenciado`

## Running LicencIAdo
Run the CLI utility in this repo: `python3 cli.py`

You can also use the interface in the `model.py` class. 