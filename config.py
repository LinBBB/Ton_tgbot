# config.py
BOT_TOKEN = '6726806938:AAGlgL34xJK-6BmuUe9m-SSCACsisQW_aCY'
DEPOSIT_ADDRESS = "UQAvHRt89olajfs1J09d3BHIWzYUis7Ho2eWze00y7Q4wSU2"
API_KEY = '77113e8d2a4ddf075d9290b90bd9a107086364f70b88ebecd386e8f1cbc504ee'
RUN_IN_MAINNET = False  # Switch True/False to change mainnet to testnet

if RUN_IN_MAINNET:
    API_BASE_URL = 'https://toncenter.com'
else:
    API_BASE_URL = 'https://testnet.toncenter.com'



MANIFEST_URL = {
  "url": "https://github.com/XaBbl4/pytonconnect",
  "name": "PyTonConnect",
  "iconUrl": "https://raw.githubusercontent.com/XaBbl4/pytonconnect/main/pytonconnect.png"
}