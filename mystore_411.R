source('C:/Users/Zheng/Downloads/scrape_function.R')

geo_key = 'AIzaSyCahybZqELJlJAWmQ3p-dTRBlNtuLfHr34'

topProv = c('Ontario', 'Nova%20Scotia', 'New%20Brunswick', 'British%20Columbia',
    'Alberta','Quebec')

secProv = c('Manitoba','Saskatchewan',
    'Newfoundland%20and%20Labrador', 'Newfoundland', 'Prince%20Edward%20Island')

acura_data = scrape_mystore411(id = '676', store_name = 'acura', 
    page_state = 'single', key = key)