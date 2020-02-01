import PySimpleGUI as sg
from pkg.corpusaccess import (
    corpusaccess,
)  # TODO: should this be done in __init__.py somehow?

corpus_path = "data/corpus/UofO_Courses.yaml"  # temp


def launch():
    # some code snippets for UI elements taken from demos at https://pysimplegui.readthedocs.io/
    # built in colour scheme
    sg.theme("Reddit")

    # settings layouts
    model_layout = [
        [sg.Radio("Boolean", "model", default=True, font=("Arial", 14))],
        [sg.Radio("Vector Space", "model", font=("Arial", 14))],
    ]

    corpus_layout = [
        [sg.Radio("uOttawa Catalogue", "corpus", default=True, font=("Arial", 14))],
        [sg.Radio("Reuters", "corpus", disabled=True, font=("Arial", 14))],
    ]

    dictionary_layout = [
        [sg.Checkbox("Stopword Removal", default=True, font=("Arial", 14))],
        [sg.Checkbox("Stemming", default=True, font=("Arial", 14))],
        [sg.Checkbox("Normalization", default=True, font=("Arial", 14))],
    ]

    # results table info
    headings = ["DocID", "Title", "Excerpt", "Score"]
    raw_data = []
    data = []

    # popup that shows full text of document on click
    def DocPopup(doc):
        text = str(doc[0]) + ": " + str(doc[1]) + "\n" + str(doc[2])
        return sg.PopupScrolled(text, title=doc[1], font=("Arial", 12), size=(64, None))

    # window layout
    layout = [
        [sg.Text("Minerva Search Engine", font=("Arial", 22, "bold"))],
        [
            sg.Text("Query:", key="query", font=("Arial", 14)),
            sg.InputText("", font=("Arial", 14), focus=True),
            sg.Button("Search", font=("Arial", 14)),
        ],
        [sg.Text("")],
        [
            sg.Frame("Corpus", corpus_layout, font=("Arial", 16, "bold")),
            sg.Frame("Models", model_layout, font=("Arial", 16, "bold")),
            sg.Frame(
                "Dictionary Building", dictionary_layout, font=("Arial", 16, "bold")
            ),
        ],
        [sg.Text("")],
        [
            sg.Text("Results", font=("Arial", 16, "bold")),
            sg.Text(
                "",
                font=("Arial", 14, "italic"),
                key="suggestion",
                text_color="red",
                size=(50, 1),
            ),
        ],
        [
            sg.Table(
                values=data,
                headings=headings,
                font=("Arial", 12),
                header_font=("Arial", 14, "bold"),
                bind_return_key=True,
                num_rows=8,
                alternating_row_color="#d3d3d3",
                auto_size_columns=False,
                col_widths=[8, 16, 32, 8],
                justification="center",
                key="_table_",
            )
        ],
        [
            sg.Text(
                "Double click on a row to view the full text.",
                font=("Arial", 12, "italic"),
            )
        ],
        [sg.Button("Exit", font=("Arial", 14), button_color=("white", "grey"))],
    ]

    # creating window
    window = sg.Window("Minerva Search Engine", layout)

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
            # TODO: create Context object and send it to some router (or something), and handle result.

            # some fake result
            doc_ids = [587, 577, 572]

            raw_data = corpusaccess.access(corpus_path, doc_ids)

            # need to save it in data so I can access it again for popup
            data = clean_data(raw_data)

            window.FindElement("_table_").Update(values=data)

            # window["suggestion"].Update("Did you mean: <spelling correction for " + values[0] + ">")

        elif event is "_table_":
            print("Opening document")

            doc = data[values[event][0]]
            DocPopup(doc)

        else:
            print(event)

    window.Close()


# turn it into an array so it can be displayed in Table
def clean_data(raw_data):
    data = []
    for d in raw_data:
        # DocID, Title, Excerpt, Score
        data.append(
            [
                d.id,
                str(d.course.faculty) + " " + str(d.course.code),
                d.course.contents,
                "score",
            ]
        )
    return data
