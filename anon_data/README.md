First, create the file structure, download the files and get python ready:

``` bash
sudo sh prepare_env.sh
```

Assuming that works, start your venv and install the requirements:

```bash
source venv/bin/activate
pip3 install -r requirements
```


Then run this to loop through the sample CSV files and create new, 'anonymised' files in the `anon_data` folder

```bash
sudo python3 -m anon_csv_data.py
```
