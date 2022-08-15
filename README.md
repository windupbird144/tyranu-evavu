### Set up Python

`python -m venv .venv chmod +x .venv/bin/activate . .venv/bin/activate pip install -r requirements.txt`

### Simulate games of Tyranu Evavu to collect stats

Results will be saved to stats.npy or any other file you provide as an argument. The file keeps running until you keyboard interrupt (press CTRL+C from the same terminal you run the python script)

`python analysis.py stats.npy`

### Analyse your stats file

`python analysis.py stats.npy --stats`

### Run the card counter (locally)

`npm run dev`

### Build the card counter

`npm run build`
