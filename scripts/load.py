##########################################################
# pdf-to-csv
import tabula

for year in [2016,2017,2018]:
    print('Processing year ' + str(year))
    pdf = './data/bieg-' + str(year) + '.pdf'
    csv = './data/bieg-' + str(year) + '.csv'
    df = tabula.read_pdf(pdf, lattice=True, pages='all', area = [20, 0, 100, 100], relative_area = True, pandas_options={'header': None})
    df.columns = ['place', 'id', 'name', 'surname', 'location', 'team', 'birthYear', 'category', 'place2', 'M', 'K', 'half-time', 'time', 'netto-time']
    if (year == 2017):
        df = df[:-4] # In 2017 there were 3 disqualified participants and they had place 'DSQ' which is not of type int
    else:
        df = df[:-1]
    df = df.fillna({'place': -1, 'id': -1, 'name': '', 'surname': '', 'location': '', 'team': '',
                   'birthYear': -1, 'category': '', 'place2': -1, 'M': -1, 'K': -1, 
                    'half-time': '', 'time': '', 'netto-time': ''})
    df = df.astype({'place': int, 'id': int, 'name': str, 'surname': str, 'location': str, 'team': str, 'birthYear': int, 'category': str, 'place2': int, 'M': int, 'K': int, 'half-time': str, 'time': str, 'netto-time': str})
    df.to_csv(csv, ';', index=False)
    
    # Replacing new-lines in cell on spaces
    file = open(csv, 'rb')
    content = file.read()
    content = content.replace(b'\r', b' ')
    content = content.replace(b' \n', b'\r\n')
    file.close()
    file = open(csv, 'wb')
    file.write(content)
    file.close()
	
##########################################################
# read dataset to numpy structured array
import pandas
df = pandas.read_csv('./data/bieg-2018.csv', ';')
df = df.astype({'place': int, 'id': int, 'name': str, 'surname': str, 'location': str, 'team': str, 'birthYear': int, 'category': str, 'place2': int, 'M': int, 'K': int, 'half-time': str, 'time': str, 'netto-time': str})
data = df.to_records(index=False)





