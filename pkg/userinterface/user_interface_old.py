import PySimpleGUI as sg
# code snippets taken from various demos at https://pysimplegui.readthedocs.io/

def launch():
    sg.theme('LightGrey1')   # colour scheme

    # Results Table:
    # headings = ['DocID', 'Title', 'Excerpt', 'Score'] # clicking doc id opens document
    # header =  [[sg.Text('  ')] + [sg.Text(h, size=(16,1)) for h in headings]]

    headers = [sg.Text('DocID', size=(8,1), font=('Arial', 14, 'bold'), justification="center"), sg.Text('Title', size=(16,1), font=('Arial', 14, 'bold'), justification="center"), sg.Text('Excerpt', size=(32,1), font=('Arial', 14, 'bold'), justification="center"), sg.Text('Score', size=(8,1), font=('Arial', 14, 'bold'), justification="center")]

    # one row in table
    def Row(doc_id, title, excerpt, score):
        return [sg.Button(doc_id, key=("open_doc-" + str(doc_id)), size=(8, 1), font=('Arial', 14), tooltip=("Open Document " + str(doc_id)), button_color=('black', 'white')), sg.Text(title, size=(16,1), font=('Arial', 14)), sg.Text(excerpt, size=(32,1), font=('Arial', 14)), sg.Text(score, size=(8,1), font=('Arial', 14), justification="center")]

    # popup that shows full text of document on click
    def DocPopup(doc):
        return sg.Popup(doc + ": full text goes here!", title=doc, custom_text="Done", font=('Arial', 14))

    # data = [Row(100,"My Title","Lorem Ipsum excerpt from corpus.",4.5), Row(428,"Another Title","Lorem Ipsum excerpt from corpus.",4.5), Row(472,"Third title","Lorem Ipsum excerpt from corpus.",4.5)]
    data = []

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

    results_layout = [headers, Row(100,"My Title","Lorem Ipsum excerpt from corpus.",4.5), Row(428,"Another Title","Lorem Ipsum excerpt from corpus.",4.5), Row(472,"Third title","Lorem Ipsum excerpt from corpus.",4.5)]


    # window layout
    layout = [  [sg.Text('Minerva Search Engine', font=('Arial', 22, 'bold'))],
                [sg.Text('Query:', key="query", font=('Arial', 14)), sg.InputText('Enter Query Here', font=('Arial', 14)), sg.Button('Search', font=('Arial', 14))],
                [sg.Text('')],
                [sg.Frame('Corpus', corpus_layout, font=('Arial', 16, 'bold')), sg.Frame('Models', model_layout, font=('Arial', 16, 'bold')), sg.Frame('Dictionary Building', dictionary_layout, font=('Arial', 16, 'bold'))],
                [sg.Text('')],
                [sg.Text('Results', font=('Arial', 16, 'bold')), sg.Text('', font=('Arial', 14, 'italic'), key="suggestion", text_color='red', size=(50, 1))],
                [sg.Frame('', results_layout, font=('Arial', 14), key="results")],
                [sg.Text('')],
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
            print(values)
            # something like -> results = router(values)
            results = dummyReturn(values[0])
            for r in results:
                results_layout += Row(r[0],r[1],r[2],r[3])
            
            window["suggestion"].Update("Did you mean: " + values[0])
            window["results"].layout = results_layout

        elif "open_doc-" in event:
            print("Open document")
            doc = event.strip("open_doc-")
            # content = corpus_access.fetch(doc)
            # print(docid)
            DocPopup(doc)
            
        else:
            print(event)
            # 

    window.Close()

def dummyReturn(q):
    return [[200, "dummy title " + q, "dummy excerpt", 10],[210, "dummy title " + q, "dummy excerpt", 10],[220, "dummy title " + q, "dummy excerpt", 10]]