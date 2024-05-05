import os
import asyncio
import yaml
from pyppeteer import launch
from datetime import datetime

# Add stealth plugin and use defaults (all tricks to hide puppeteer usage)
from pyppeteer_stealth import stealth

state_codes = {
  'Alabama': 'AL',
  'Alaska': 'AK',
  'Arizona': 'AZ',
  'Arkansas': 'AR',
  'California': 'CA',
  'Colorado': 'CO',
  'Connecticut': 'CT',
  'District of Columbia': 'DC',
  'Delaware': 'DE',
  'Florida': 'FL',
  'Georgia': 'GA',
  'Hawaii': 'HI',
  'Idaho': 'ID',
  'Illinois': 'IL',
  'Indiana': 'IN',
  'Iowa': 'IA',
  'Kansas': 'KS',
  'Kentucky': 'KY',
  'Louisiana': 'LA',
  'Massachusetts': 'MA',
  'Maryland': 'MD',
  'Maine': 'ME',
  'Michigan': 'MI',
  'Minnesota': 'MN', 
  'Mississippi': 'MS',
  'Missouri': 'MO',
  'Montana': 'MT',
  'Nebraska': 'NE',
  'Nevada': 'NV',
  'New Hampshire': 'NH',
  'New Jersey': 'NJ',
  'New Mexico': 'NM',
  'New York': 'NY',
  'North Carolina': 'NC',
  'North Dakota': 'ND',
  'Ohio': 'OH',
  'Oklahoma': 'OK',
  'Oregon': 'OR',
  'Pennsylvania': 'PA',
  'Rhode Island': 'RI',
  'South Carolina': 'SC',
  'South Dakota': 'SD',
  'Tennessee': 'TN',
  'Texas': 'TX',
  'Utah': 'UT',
  'Vermont': 'VT',
  'Virginia': 'VA',
  'Washington': 'WA',
  'West Virginia': 'WV',
  'Wisconsin': 'WI',
  'Wyoming': 'WY'
}

async def check_sf_parking_tickets(plate_number: str, state_plate: str):
    try:

        print(f'--- START SESSION {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---')
        print(f'Checking for SFMTA parking tickets for Plate Number {plate_number}, State {state_plate}')
        browser = await launch(headless=True)
        page = await browser.newPage()
        await stealth(page)

        await page.goto('https://wmq.etimspayments.com/pbw/include/sanfrancisco/input.jsp')

        # ----- FIRST PAGE -----
        print('New Page URL:', page.url)

        await page.type('input[name=plateNumber]', plate_number)
        await page.select('select[name=statePlate]', state_plate)
        await page.click('input[name="submit"]')

        # ----- SECOND PAGE -----
        await page.waitForSelector('input[value=indAmounts]')
        print('New Page URL:', page.url)

        await page.evaluate('(selector) => document.querySelector(selector).click()', 'input[name=payTheseItems]')
        total_payment_element = await page.waitForXPath("//font[contains(text(), 'Total Payment')]")
        total_payment_value_element = (await total_payment_element.xpath('./following-sibling::font'))[0]
        total_payment_value = await page.evaluate('(el) => el.textContent', total_payment_value_element)
        
        pay_these_items_elements = await page.querySelectorAll('input[name="payTheseItems"]')
        
        if len(pay_these_items_elements) == 0:
            print("Yay! No tickets found.")
        else:
            print(f"Oop, we found {len(pay_these_items_elements)} tickets. You might want to pay these lol")
            for i, element in enumerate(pay_these_items_elements, start=1):
                value = await page.evaluate('(el) => el.value', element)
                print(f"- Ticket #{i}: {value}")
            
            print(f"Total Payment Required: {total_payment_value}")
                
        print(f'--- END SESSION {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ---')

        await browser.close()

    except Exception as e:
        print(f"ERROR: {e}")
        print(f'--- END SESSION {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ---')

        await browser.close()

if __name__ == "__main__":
    
    my_data_path = os.path.expanduser(os.path.abspath('my_data.yaml'))
    with open("my_data.yaml", "r") as file:
        my_data = yaml.safe_load(file)

    PLATE_NUMBER = my_data["car_license"] 
    STATE_PLATE = state_codes[my_data["car_state"]]

    asyncio.run(check_sf_parking_tickets(PLATE_NUMBER, STATE_PLATE))
