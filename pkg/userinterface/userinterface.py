import PySimpleGUI as sg
from os import path

from pkg.context import Context
from pkg.corpusaccess import CorpusAccessor
from pkg.editdistance import EditDistance
from pkg.dictionary import Dictionary
from pkg.index import IndexAccessor, BigramIndexAccessor, WeightedIndexAccessor


# code snippets taken from various demos at https://pysimplegui.readthedocs.io/
def launch():
    # results table info
    headings = ["DocID", "Title", "Excerpt", "Score"]
    data = []

    # query data for edit distance and 'resending' query
    original_query = ""
    updated_query = ""
    suggestions = []

    # built in colour scheme
    sg.theme("Reddit")

    # settings layouts
    model_layout = [
        [
            sg.Radio(
                "Boolean", "model", default=True, font=("Arial", 14), key="_boolean_"
            )
        ],
        [sg.Radio("Vector Space", "model", font=("Arial", 14), key="_vsm_")],
    ]

    corpus_layout = [
        [
            sg.Radio(
                "uOttawa Catalogue",
                "corpus",
                default=True,
                font=("Arial", 14),
                key="_uottawa_",
            )
        ],
        [
            sg.Radio(
                "Reuters", "corpus", disabled=True, font=("Arial", 14), key="_reuters_"
            )
        ],
    ]

    dictionary_layout = [
        [
            sg.Checkbox(
                "Stopword Removal", default=True, font=("Arial", 14), key="_stopword_"
            )
        ],
        [sg.Checkbox("Stemming", default=False, font=("Arial", 14), key="_stemming_")],
        [
            sg.Checkbox(
                "Normalization", default=True, font=("Arial", 14), key="_normalization_"
            )
        ],
    ]

    # popup that shows full text of document
    def DocPopup(doc):
        text = str(doc[0]) + ": " + str(doc[1]) + "\n" + str(doc[2])
        return sg.PopupScrolled(
            text, title=doc[1], font=("Arial", 12), size=(64, None), keep_on_top=True
        )

    # popup that shows top N suggestions per query term
    def SuggestionPopup(suggestions):
        text = ""

        for term in suggestions:
            if suggestions[term] != []:
                text += term + " : "
                for s in suggestions[term]:
                    text += s + ", "
                text += "\n"

        return sg.PopupScrolled(
            text,
            title="Suggestions for " + original_query,
            font=("Arial", 12),
            size=(64, None),
            keep_on_top=True,
        )

    # window layout
    layout = [
        [sg.Text("Minerva Search Engine", font=("Arial", 22, "bold"))],
        [
            sg.Text("Query:", font=("Arial", 14)),
            sg.InputText("", font=("Arial", 14), focus=True, key="_query_",),
            sg.Button("Search", font=("Arial", 14), bind_return_key=True),
        ],
        [sg.Text("")],
        [
            sg.Frame("Corpus", corpus_layout, font=("Arial", 16, "bold")),
            sg.Frame("Model", model_layout, font=("Arial", 16, "bold")),
            sg.Frame(
                "Dictionary Building", dictionary_layout, font=("Arial", 16, "bold")
            ),
        ],
        [sg.Text("")],
        [sg.Text("Results", font=("Arial", 16, "bold"))],
        [
            sg.Button(
                "Showing results for <updated_query>. Click here to search for <original_query>.",
                font=("Arial", 12),
                size=(64, 1),
                visible=False,
                disabled_button_color=("white", None),
                key="_resend_",
            )
        ],
        [sg.Text("", font=("Arial", 5))],
        [
            sg.Button(
                "Click here to see more suggestions.",
                font=("Arial", 12),
                visible=False,
                pad=((0, 50)),
                key="_suggestions_",
            )
        ],
        [sg.Text("", font=("Arial", 5))],
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
            original_query = values["_query_"]
            print("Original query: " + str(original_query))

            # create context object
            ctx = construct_context(values)

            # get weighted edit distance suggestions for query
            suggestions = EditDistance(ctx).edit_distance(original_query)
            print(suggestions)

            # update edit distance related UI elements
            if not suggestions:
                # if theres no suggestions (all query terms were in dictionary or regex terms), don't display suggestion related UI elements
                window["_resend_"].set_size((len(original_query) + 25, None))
                window["_resend_"].Update(
                    text=("Showing results for '" + original_query + "'."),
                    disabled=True,
                    visible=True,
                )
                window["_suggestions_"].Update(visible=False)
                updated_query = original_query
            else:
                # if theres suggestions (one or more query term was not in dictionary)
                # construct the new query
                updated_query = ""
                for term in original_query.split():
                    if not (term in suggestions):
                        updated_query += term + " "
                    else:
                        updated_query += suggestions[term][0] + " "

                # display suggestion related UI elements
                window["_resend_"].set_size(
                    (len(original_query) + len(updated_query) + 40, None)
                )
                window["_resend_"].Update(
                    text=(
                        "Showing results for '"
                        + updated_query
                        + "'. Click here to search for '"
                        + original_query
                        + "'."
                    ),
                    disabled=False,
                    visible=True,
                )
                window["_suggestions_"].Update(visible=True)

            # TODO: Call chosen search model to get results.
            if values["_boolean_"]:
                print("Calling Boolean with query: " + updated_query)
                results = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # temp dummy data
            elif values["_vsm_"]:
                print("Calling VSM with query: " + updated_query)
                results = [
                    510,
                    520,
                    530,
                    540,
                    550,
                    560,
                    570,
                    580,
                    590,
                    600,
                ]  # temp dummy data

            # get returned documents from corpus accessor
            corpus_accessor = CorpusAccessor(ctx)
            documents = corpus_accessor.access(ctx, results)

            # format documents for table UI element and update table
            data = []
            for d in documents:  # TODO: handle score from VSM / no score from Bool
                data.append(
                    [
                        d.id,
                        str(d.course.faculty) + " " + str(d.course.code),
                        d.course.contents,
                        "score",
                    ]
                )

            window["_table_"].Update(values=data)

        elif event is "_table_":
            print("Opening document")

            doc = data[values[event][0]]
            DocPopup(doc)

        elif event is "_suggestions_":
            print("Displaying top N suggestions")
            SuggestionPopup(suggestions)

        elif event is "_resend_":
            print("Resending query: " + original_query)
            # TODO: handle 'resending' a query

        else:
            print(event)

    window.Close()


# returns a Context object with the user's selections
def construct_context(values):
    # once we have multiple corpora, these variables will be defined based on user selection: values["_uottawa_"] or values["_reuters_"]
    corpus_path = path.abspath("data/corpus/UofO_Courses.yaml")
    dictionary_path = path.abspath("data/dictionary/UofOCourses.txt")
    inverted_index_path = path.abspath("data/index/UofO_Courses.yaml")

    ctx = Context(
        corpus_path,
        dictionary_path,
        inverted_index_path,
        enable_stopwords=values["_stopword_"],
        enable_stemming=values["_stemming_"],
        enable_normalization=values["_normalization_"],
    )
    # eager load if not already in memory
    CorpusAccessor(ctx)
    Dictionary(ctx)
    IndexAccessor(ctx)
    BigramIndexAccessor(ctx)
    WeightedIndexAccessor(ctx)
    return ctx
