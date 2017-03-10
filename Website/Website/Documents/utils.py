import json
from json import JSONEncoder

class MyEncoder(JSONEncoder):
    def default(self, object):
        return str(object)

ApprovalAgencyChoices = (
    ("AA1", "AA1"),
    ("AA2", "AA2"),
    ("AA3", "AA3")
)

StatusChoices = (
    ("Valid", "Valid"),
    ("Sold", "Sold")
)

DocumentTypeChoices = (
    ("Dtype1", "Dtype1"),
    ("Dtype2", "Dtype2")
)

AssetTypeChoices = (
    ("Atype1", "Atype1"),
    ("Atype2", "Atype2")
)