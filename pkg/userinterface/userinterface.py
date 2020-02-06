import PySimpleGUI as sg
from os import path

from pkg.context import Context
from pkg.corpusaccess import CorpusAccessor
from pkg.editdistance import EditDistance


def launch():
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
            sg.InputText(
                "Example Query operoting system lienar", font=("Arial", 14), focus=True
            ),
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
        [sg.Text("Results", font=("Arial", 16, "bold"))],
        [
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
                alternating_row_color="grey",
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
            query = values[0]
            print("Search for " + str(query))

            corpus_path = path.realpath("data/corpus/UofO_Courses.yaml")
            dictionary_path = path.realpath("data/dictionary/UofOCourses.txt")
            inverted_index_path = path.realpath("data/index/UofO_Courses.yaml")

            ctx = Context(corpus_path, dictionary_path, inverted_index_path)
            corpus_accessor = CorpusAccessor(ctx)

            # call some search function w/ query

            results = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # temp dummy data
            documents = corpus_accessor.access(ctx, results)

            data = []
            for d in documents: # TODO: handle score
                data.append(
                    [
                        d.id,
                        str(d.course.faculty) + str(d.course.code),
                        d.course.contents,
                        "score",
                    ]
                )

            window.FindElement("_table_").Update(values=data)

            suggestions = EditDistance(ctx).edit_distance(query)
            print(suggestions)

            window["suggestion"].Update("Did you mean:")

            # for query_term, suggestion in suggestions:
            #     if suggestion not []:
            #         sg.Combo([query_term, ])

            layout = [[sg.Combo(['choice 1', 'choice 2'])]]

        elif event is "_table_":
            print("Opening document")

            doc = data[values[event][0]]
            DocPopup(doc)

        else:
            print(event)

    window.Close()
