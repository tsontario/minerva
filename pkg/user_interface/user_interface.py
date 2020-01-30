import PySimpleGUI as sg
# code snippets taken from various demos at https://pysimplegui.readthedocs.io/

def launch():
    # built in colour scheme
    sg.theme('Reddit')   

    # settings layouts
    model_layout = [    [sg.Radio('Boolean', "model", default=True, font=('Arial', 14))], [sg.Radio('Vector Space', "model", font=('Arial', 14))]
    ]

    corpus_layout = [   [sg.Radio('uOttawa Catalogue', "corpus", default=True, font=('Arial', 14))], [sg.Radio('Reuters', "corpus", disabled=True, font=('Arial', 14))]
    ]

    dictionary_layout = [   [sg.Checkbox('Stopword Removal', default=True, font=('Arial', 14))], [sg.Checkbox('Stemming', default=True, font=('Arial', 14))], [sg.Checkbox('Normalization', default=True, font=('Arial', 14))]
    ]
    
    # results table info
    headings = ['DocID', 'Title', 'Excerpt', 'Score'] 
    data = []
    
    # popup that shows full text of document on click
    def DocPopup(doc):
        text = str(doc[0]) + ": " + str(doc[1]) + "\n" + str(doc[2])
        return sg.PopupScrolled(text, title=doc[1], font=('Arial', 12), size=(64, None))

    # window layout
    layout = [  [sg.Text('Minerva Search Engine', font=('Arial', 22, 'bold'))],
                [sg.Text('Query:', key="query", font=('Arial', 14)), sg.InputText('', font=('Arial', 14), focus=True), sg.Button('Search', font=('Arial', 14))],
                [sg.Text('')],
                [sg.Frame('Corpus', corpus_layout, font=('Arial', 16, 'bold')), sg.Frame('Models', model_layout, font=('Arial', 16, 'bold')), sg.Frame('Dictionary Building', dictionary_layout, font=('Arial', 16, 'bold'))],
                [sg.Text('')],
                [sg.Text('Results', font=('Arial', 16, 'bold')), sg.Text('', font=('Arial', 14, 'italic'), key="suggestion", text_color='red', size=(50, 1))],
                [sg.Table(values=data, headings=headings, font=('Arial', 12), header_font=('Arial', 14, 'bold'), bind_return_key=True, num_rows=8, alternating_row_color='grey', auto_size_columns=False, col_widths=[8,16,32,8], justification='center', key='_table_')],
                [sg.Text('Double click on a row to view the full text.', font=('Arial', 12, 'italic'))],
                [sg.Button('Exit', font=('Arial', 14), button_color=('white', 'grey'))]
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

        elif event is "Search":
            print("Search for " + str(values[0]))
            # TODO: create config object and send it to some router (or something), and handle result.
            data = dummyReturn(values[0])

            window.FindElement('_table_').Update(values = data)
        
            window["suggestion"].Update("Did you mean: <spelling correction for " + values[0] + ">")

        elif event is "_table_":
            print("Opening document")

            doc = data[values[event][0]]
            DocPopup(doc)
            
        else:
            print(event)

    window.Close()

# temp dummy data
def dummyReturn(q):
    return [[200, "Title " + q, "Some excerpt", 0.1],[210, "Title " + q, "Some excerpt", 0.1],[220, "Title " + q, "Some excerpt", 0.1],[230, "Title " + q, "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent fermentum et mauris sed dictum. Maecenas sed aliquam nisl. In pharetra eget augue ut tincidunt. Curabitur id ante id nulla sagittis molestie. Nunc vel congue arcu. Aliquam eleifend, purus in lobortis suscipit, justo risus tristique elit, eget dignissim lacus velit volutpat libero. Nullam id cursus nisl, sit amet tincidunt est. Aenean rhoncus ornare rhoncus. Nulla massa erat, dignissim eget lobortis et, consequat ut ipsum. Aenean maximus velit sed sapien tempus, a euismod urna maximus. Proin lectus nunc, euismod vel ultrices in, tempus ut lacus. Cras sed tellus sed libero bibendum fringilla. Nam vel metus odio. Morbi dictum fringilla massa.", 0.1]]