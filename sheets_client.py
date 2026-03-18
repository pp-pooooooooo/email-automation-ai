import gspread

def get_sheet(creds, sheet_url):
    gc = gspread.authorize(creds)
    return gc.open_by_url(sheet_url).sheet1