import os
from project.utils import constants
import pandas as pd


def get_team():
    linkedin_path = os.path.join(constants.data_dir, constants.linkedinfile)
    linkedin_details = pd.read_csv(linkedin_path)
    images = linkedin_details['imageurl'].tolist()
    urls = linkedin_details['url'].tolist()
    names = linkedin_details['name'].tolist()
    designations = linkedin_details['designation'].tolist()
    return images, urls, names, designations
