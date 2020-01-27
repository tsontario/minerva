import PySimpleGUI as sg
# code snippets taken from various demos at https://pysimplegui.readthedocs.io/

def launch():
    sg.theme('LightGrey1')   # colour scheme

    # Results Table:
    # headings = ['DocID', 'Title', 'Excerpt', 'Score'] # clicking doc id opens document
    # header =  [[sg.Text('  ')] + [sg.Text(h, size=(16,1)) for h in headings]]

    # header = [sg.Text('   DocID', size=(16,1), font=('Arial', 14, 'bold'))], [sg.Text('   Title', size=(16,1), font=('Arial', 14, 'bold'))], [sg.Text('   Excerpt', size=(16,1), font=('Arial', 14, 'bold'))], [sg.Text('   Score', size=(16,1), font=('Arial', 14, 'bold'))]

    # settings layouts
    model_layout = [
                    [sg.Radio('Boolean', "model", default=True, font=('Arial', 14))], [sg.Radio('Vector Space', "model", font=('Arial', 14))]
                ]

    corpus_layout = [
                    [sg.Radio('uOttawa Catalogue', "corpus", default=True, font=('Arial', 14))], [sg.Radio('Reuters', "corpus", disabled=True, font=('Arial', 14))]
                ]

    dictionary_layout = [
                    [sg.Checkbox('Stopword Removal', default=True, font=('Arial', 14))], [sg.Checkbox('Stemming', default=True, font=('Arial', 14))], [sg.Checkbox('Normalization', default=True, font=('Arial', 14))]
                ]

    results_layout = []


    # window layout
    layout = [  [sg.Text('Minerva Search Engine', font=('Arial', 22, 'bold'))],
                [sg.Text('Query:', key='query', font=('Arial', 14)), sg.InputText('Enter Query Here', font=('Arial', 14)), sg.Button('Go', font=('Arial', 14))],
                [sg.Text('')],
                [sg.Frame('Corpus', corpus_layout, font=('Arial', 16, 'bold')), sg.Frame('Models', model_layout, font=('Arial', 16, 'bold')), sg.Frame('Dictionary Building', dictionary_layout, font=('Arial', 16, 'bold'))],
                [sg.Text('')],
                [sg.Text('Results', font=('Arial', 16, 'bold'), key='res')],
                [sg.Frame('Results', results_layout, font=('Arial', 16, 'bold'), key='result_box')],
                #[sg.Text('DocID', font=('Arial', 14, 'bold')), sg.Text('          Title', font=('Arial', 14, 'bold')), sg.Text('          Excerpt', font=('Arial', 14, 'bold')), sg.Text('          Score', font=('Arial', 14, 'bold'))],
                [sg.Button('Exit', font=('Arial', 14))]
                 ]
    
    # creating window
    window = sg.Window('Minerva Search Engine', layout)
    
    # event loop
    while True:
        event, values = window.Read()
        if event is None:
            break
        elif event is "Exit":
            print("Exiting")
            window.Close()
        elif event is "Go":
            print(values)
        else:
            print(event)

    window.Close()
