from aiohttp import request
import requests

print(
    requests.get(
        "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=602573158594-la6m0t8kqd48aoupkr17hqt776ofd6qg.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&state=uepEkxjYdI9oASnPFcN1SrYdbMgCUK&prompt=consent&access_type=offline"
    ).content
)
