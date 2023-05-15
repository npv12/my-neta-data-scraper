# Data Scarper 

## Scrapes the website https://myneta.info
To run the script you would need the dependency as mentioned in requirements.txt
To install the dependency, use 
```bash
pip install -r requirements.txt
```

Then you can run the script using 
```bash
python main.py
```

This will scrape the data and store all data for state of orissa. 

## Hacking
In case you want data for a different state, you can start with changing the url from 

```bash
url = f"{base_url}/state_assembly.php?state=Odisha"
```

to 
```bash
url = f"{base_url}/state_assembly.php?state=Gujarat"
```

and also change this line
```bash
year = href.split("/")[1].lower().strip("odisha").strip("orissa")
```

to 

```bash
year = href.split("/")[1].lower().strip("gujarat")
```
If your state has more instances of names, add more .strip at the end as in the case of odisha

In case you need more assistance, feel free to open an issue. 