import os
from dotenv import load_dotenv
from urllib.request import urlopen 
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import pandas as pd

# 환경 변수 로드
load_dotenv()
api_url = os.getenv("OPENAPI_URL")
api_key = os.getenv("OPENAPI_KEY")

def get_dataset(url, api_key):
    number = 10
    page_no = 1
    all_items = []

    while True:
        request_url = f"{url}?serviceKey={api_key}&numOfRows={number}&pageNo={page_no}"
        result = urlopen(request_url)
        soup = BeautifulSoup(result, 'lxml-xml')
        items = soup.find_all('item')

        if not items:
            break  # Stop if no items are found

        all_items.extend(items)
        page_no += 1  # Increment page number to fetch next set of items

    return all_items

# Fetch dataset
dataset = get_dataset(api_url, api_key)
print(len(dataset))

# Prepare list to store extracted data
data = []

# Iterate over dataset to extract information
for item in dataset:
    extracted_data = {
        'Title': item.title.string.strip() if item.title and item.title.string else '',
        'Alternative Title': item.alternativeTitle.string.strip() if item.alternativeTitle and item.alternativeTitle.string else '',
        'Creator': item.creator.string.strip() if item.creator and item.creator.string else '',
        'RegDate': item.regDate.string.strip() if item.regDate and item.regDate.string else '',
        'CollectionDb': item.collectionDb.string.strip() if item.collectionDb and item.collectionDb.string else '',
        'SubjectCategory': item.subjectCategory.string.strip() if item.subjectCategory and item.subjectCategory.string else '',
        'SubjectKeyword': item.subjectKeyword.string.strip() if item.subjectKeyword and item.subjectKeyword.string else '',
        'Extent': item.extent.string.strip() if item.extent and item.extent.string else '',
        'Description': item.description.string.strip() if item.description and item.description.string else '',
        'SpatialCoverage': item.spatialCoverage.string.strip() if item.spatialCoverage and item.spatialCoverage.string else '',
        'Temporal': item.temporal.string.strip() if item.temporal and item.temporal.string else '',
        'Person': item.person.string.strip() if item.person and item.person.string else '',
        'Language': item.language.string.strip() if item.language and item.language.string else '',
        'SourceTitle': item.sourceTitle.string.strip() if item.sourceTitle and item.sourceTitle.string else '',
        'ReferenceIdentifier': item.referenceIdentifier.string.strip() if item.referenceIdentifier and item.referenceIdentifier.string else '',
        'Rights': item.rights.string.strip() if item.rights and item.rights.string else '',
        'CopyrightOthers': item.copyrightOthers.string.strip() if item.copyrightOthers and item.copyrightOthers.string else '',
        'URL': item.url.string.strip() if item.url and item.url.string else '',
        'Contributor': item.contributor.string.strip() if item.contributor and item.contributor.string else '',
        'SubDescription': item.subDescription.string.strip() if item.subDescription and item.subDescription.string else ''
    }
    data.append(extracted_data)

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)
# Save the DataFrame to a CSV file
df.to_csv('dataset.csv', index=False)

# Optionally, print a message confirming the file has been saved
print("Data saved to 'dataset.csv'")