# BBC Monitoring API Python Wrapper
A python wrapper for the BBC monitoring API. The wrapper currently has limitted ans specific functionality. Current use cases are limitted to searching for text within headlines and extracting the text from an article into a single string. Articles can also be searche dby ID, if IDs are known. The code includes a notebook demonstrating the extraction of a list of articles relating to ahandful of cities, based on the headline details.

## Requirements
* Python 3.8+
* beautifulsoup4
* tqdm
* pandas

## Code
* `api_wrapper.py`: contains the class `BBCMonitoringAPI` which interacts with bb-monitoring via the requests library. A valid API key is required for this to work.
* `error_handling.py`: provides exceptions and error messages for some of the status codes provided by the api.
* `NB1_demoing_article_extraction.ipynb`: a notebook demonstrating a usecase for the API.

## API Key and registration
Users must have a valid API key available from [bbc-monitoring](https://monitoring.bbc.co.uk/), and the account must be fully activated. The API-key should be stored in a JSON flie structured as `{"username":<username>, "password":<password>}`. A template key is provided in `data/fake_key.json`. 
