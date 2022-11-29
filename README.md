# Estimating Biases in Facial Analysis Tools
This repository includes the code for the experiments conducted for my undergraduate thesis titled *"Estimating Biases in Facial Analysis Tools"*. A copy of the final report is provided in the root directory (`report.pdf`). 

![Sample Diagram](https://drive.google.com/uc?export=view&id=1YeNcC-ENcU9_fmEq0ISZizqn_WrhbWQP)

### Dsiclaimer

Because of data privacy regulations, the contents of the CFD, NimStim and AirBnb datasets have not been included in this public repository.
For security purposes, details of the code have been omitted (such as strings containing API keys, AWS credentials or S3 bucket names).

### File Structure

The root directory of the Git repository is split into five folders:
* `analysis` – contains the Jupyter Notebooks for the data analysis. `analysis.ipynb` is used for visualisation. The `stage_1`, `stage_2` and `stage_3` notebooks implement the accuracy performance, the correlation testing and the logistic regression respectively.
* `api_processing` – contains the scripts for the API processing (in the `/Code` subdirectory) and the datasets (`/Data`). In the `/Code` subdirectory, each API has a folder assigned, which in turn contains one folder per dataset. In each of those folders, you can find the one processing script `<API_name>_processing.py`, the resulting logs and a script transforming the logs into a `.csv` file.
* `experiment` – contains data and scripts for the crowdworking experiment.
* `preprocessing` – includes the data standardisation scripts.
* `tables` – contains the `.csv` tables including the processing results. 