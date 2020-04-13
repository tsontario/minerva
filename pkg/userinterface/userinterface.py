import PySimpleGUI as sg
from os import path
from collections import defaultdict

from pkg.context import Context
from pkg.corpusaccess import CorpusAccessor
from pkg.editdistance import EditDistance
from pkg.queryexpansion import Expansion
from pkg.querycompletion import Completion
from pkg.relevancefeedback import RelevanceFeedback
from pkg.dictionary import Dictionary
from pkg.index import IndexAccessor, BigramIndexAccessor, WeightedIndexAccessor
from pkg.vsm import VectorSpaceModel
from pkg.booleanretrieval import Parser, Evaluator


# code snippets taken from various demos at https://pysimplegui.readthedocs.io/
def launch():
    # results table info
    headings = ["Relevance", "DocID", "Title", "Topic", "Excerpt", "Score"]
    data = []
    relevance = defaultdict(lambda: [])
    # query data for edit distance and 'resending' query
    original_query = ""
    original_values = []
    updated_query = ""
    suggestions = []
    ctx = Context("", "", "")

    # for query suggestions
    next_terms = []

    # Reuters topics
    # get topics from "all-topics-strings.lc.txt"
    topic_file = path.abspath(
        path.join("data", "raw", "reuters", "all-topics-strings.lc.txt")
    )
    topics = []
    with open(topic_file) as f:
        topics = ["ALL TOPICS"] + f.read().splitlines()

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
                enable_events=True,
            )
        ],
        [
            sg.Radio(
                "Reuters",
                "corpus",
                font=("Arial", 14),
                key="_reuters_",
                enable_events=True,
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

    # window layout
    layout = [
        [sg.Text("Minerva Search Engine", font=("Arial", 22, "bold"))],
        [
            sg.Text("Query:", font=("Arial", 14)),
            sg.InputText(
                "", font=("Arial", 14), focus=True, enable_events=True, key="_query_",
            ),
            sg.Button("Search", font=("Arial", 14), bind_return_key=True),
        ],
        [
            sg.Text("Next: ", font=("Arial", 14)),
            sg.Listbox(
                values=next_terms,
                size=(30, 3),
                font=("Arial", 14),
                key="_next_",
                enable_events=True,
            ),
            sg.Text(
                "Click on a word to add it to your query.",
                font=("Arial", 12, "italic"),
            ),
        ],
        [
            sg.Text("Topic:", font=("Arial", 14)),
            sg.Combo(
                topics,
                font=("Arial", 14),
                readonly=True,
                disabled=True,
                default_value="ALL TOPICS",
                key="_topics_",
            ),
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
        [sg.Text("")],
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
                col_widths=[8, 8, 12, 8, 32, 8],
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
        [sg.Text("Relevant docs for this query", font=("Arial", 12))],
        [
            sg.Table(
                values=relevance,
                headings=headings,
                font=("Arial", 12),
                header_font=("Arial", 14, "bold"),
                bind_return_key=True,
                num_rows=4,
                alternating_row_color="#d3d3d3",
                auto_size_columns=False,
                col_widths=[8, 8, 12, 8, 32, 8],
                justification="center",
                key="_relevance_",
            )
        ],
        [sg.Button("Exit", font=("Arial", 14), button_color=("white", "grey"))],
    ]

    # creating window
    window = sg.Window("Minerva Search Engine", layout)

    # popup that shows full text of document
    def DocPopup(query, doc):
        text = ""
        if doc[0] == "not relevant":
            doc[0] = "relevant"
            RelevanceFeedback().set_relevant(query, doc)

        sections = ["DocID", "Title", "Topics", "Full Text"]
        for i in range(len(sections)):
            text += sections[i] + ": " + str(doc[i+1]) + "\n"

        return sg.PopupScrolled(
            text, title=doc[1], font=("Arial", 12), size=(64, 15), keep_on_top=True
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

    def ExpansionPopup(expansions):
        text = "Accept these expansions?\n"

        for term in expansions.items():
            text += term[0] + " -- "
            for t in term[1]:
                text += t + ", "
            text += "\n"

        sg.theme("BrownBlue")

        return sg.popup_scrolled(
            text, title="Expansions", font=("Arial", 12, "bold"), size=(64, 5), keep_on_top=True, yes_no=True
        )

    # turns edit distance UI elements on or off
    def toggle_resend(toggle):
        if toggle:
            # turn resend on
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
        else:
            # turn resend off
            window["_resend_"].set_size((len(original_query) + 25, None))
            window["_resend_"].Update(
                text=("Showing results for '" + original_query + "'."),
                disabled=True,
                visible=True,
            )
            window["_suggestions_"].Update(visible=False)

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
            original_values = values
            print("Search for query: " + str(original_query))

            topic = values["_topics_"]
            print("Chosen topic: " + topic)

            # create context object
            ctx = construct_context(values)

            # get weighted edit distance suggestions for query
            suggestions = EditDistance(ctx).edit_distance(original_query)

            # update edit distance related UI elements
            if not suggestions:
                # if theres no suggestions (all query terms were in dictionary or regex terms), don't display suggestion related UI elements
                toggle_resend(False)
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
                toggle_resend(True)
                print("Corrected query: " + updated_query)

            print("Getting expansions")
            expanded_query = updated_query
            expansions = Expansion(ctx).expand(expanded_query)

            do_expansion = "No"
            if expansions != {}:
                do_expansion = ExpansionPopup(expansions)
                print(do_expansion)
                sg.theme("Reddit")

            if do_expansion == "Yes":
                expanded_query = mix_in(expanded_query, expansions, values)

            # use chosen model to search corpus
            if values["_boolean_"]:
                data = search("Boolean", original_query, expanded_query, ctx, topic)
            elif values["_vsm_"]:
                data = search(
                    "VSM",
                    original_query,
                    expanded_query,
                    ctx,
                    topic,
                    relevance=relevance[original_query],
                )
            else:
                data = []

            window["_table_"].Update(values=data)
            relevance[original_query] = RelevanceFeedback().access(original_query)
            window["_relevance_"].Update(values=relevance[original_query])

        elif event is "_resend_":
            print("Resending query: " + original_query)

            # don't display suggestion related UI elements
            toggle_resend(False)

            print("Getting expansions")
            expanded_query = original_query
            expansions = Expansion(ctx).expand(expanded_query)

            do_expansion = "No"
            if expansions != {}:
                do_expansion = ExpansionPopup(expansions)
                print(do_expansion)
                sg.theme("Reddit")

            if do_expansion == "Yes":
                expanded_query = mix_in(expanded_query, expansions, values)

            # redo search using chosen model to search corpus
            if original_values["_boolean_"]:
                data = search("Boolean", original_query, expanded_query, ctx, topic)
            elif original_values["_vsm_"]:
                data = search(
                    "VSM",
                    original_query,
                    expanded_query,
                    ctx,
                    topic,
                    relevance=relevance[original_query],
                )
            else:
                data = []

            window["_table_"].Update(values=data)
            window["_relevance_"].Update(values=relevance[original_query])

        elif event is "_table_":
            print("Opening document")
            try:
                doc = data[values[event][0]]
                DocPopup(original_query, doc)
                window["_table_"].Update(values=data)
                window["_relevance_"].Update(values=relevance[original_query])

            except IndexError:
                # so that clicking a weird part of the table doesn't crash the application
                pass

        elif event is "_relevance_":
            print("Removing relevant doc")
            try:
                doc = relevance[original_query][values[event][0]]
                for da in data:
                    if da[1] == doc[1]:
                        da[0] = "not relevant"
                doc[0] = "not relevant"
                relevance[original_query].remove(doc)
                RelevanceFeedback().unset_relevant(original_query, doc)
                window["_table_"].Update(values=data)
                window["_relevance_"].Update(values=relevance[original_query])
            except IndexError:
                # so that clicking a weird part of the table doesn't crash the application
                pass

        elif event is "_suggestions_":
            print("Displaying edit distance suggestions")
            SuggestionPopup(suggestions)

        elif event is "_uottawa_":
            # no topics for uOttawa corpus
            window["_topics_"].Update(disabled=True)

        elif event is "_reuters_":
            # enable topics for Reuters
            window["_topics_"].Update(disabled=False)
            window["_topics_"].Update(
                readonly=True
            )  # must be done in separate Update calls

        elif event in "_query_":
            query = values["_query_"]
            if query == "" or query[-1] == " ":
                ctx = construct_context(values)
                try:
                    next_terms = Completion(ctx).complete(query.split()[-1])
                    window["_next_"].Update(values=next_terms)
                except IndexError:
                    pass
            else:
                window["_next_"].Update(values=[])

        elif event is "_next_":
            next_term = values[event][0]
            print("Adding term '" + next_term + "' to query")
            new_query = window["_query_"].Get() + next_term + " "
            window["_query_"].Update(value=new_query)
            
            ctx = construct_context(values)
            try:
                next_terms = Completion(ctx).complete(next_term)
                window["_next_"].Update(values=next_terms)
            except IndexError:
                pass

        else:
            print(event)

    window.Close()


# perform search with query / model selected by user
def search(model, original_query, modified_query, ctx, topic, relevance=None):
    corpus_accessor = CorpusAccessor(ctx)
    results = None
    if model == "VSM":
        print("Calling VSM with query: " + modified_query)
        vector_model = VectorSpaceModel(ctx)
        results = vector_model.search(ctx, modified_query, topic, relevance)
        documents = corpus_accessor.access(ctx, [r[0] for r in results])
        scores = ["{:.4f}".format(r[1]) for r in results]
        results = format_results(documents, scores, ctx)
        results = set_relevances(ctx, original_query, results)
    elif model == "Boolean":
        print("Calling Boolean with query: " + modified_query)
        parser = Parser(ctx)
        parsed = parser.parse(modified_query)
        data = Evaluator(ctx, parsed).evaluate()
        documents = corpus_accessor.access(ctx, data)
        if topic != "ALL TOPICS":
            filtered_documents = []
            for d in documents:
                if topic in d.topics:
                    filtered_documents.append(d)
            documents = filtered_documents
        scores = [1] * len(documents)
        results = format_results(documents, scores, ctx)
    return results


# format documents for table UI element
def format_results(documents, scores, ctx):
    data = []

    if ctx.corpus_type() is "reuters":
        for i in range(len(documents)):
            d = documents[i]
            data.append(
                ["", d.id, d.title, d.topics, d.body.replace("\n", " "), scores[i],]
            )
    else:
        for i in range(len(documents)):
            d = documents[i]
            data.append(
                [
                    "",
                    d.id,
                    str(d.course.faculty) + str(d.course.code) + ": " + str(d.course.title),
                    "N/A",
                    d.course.contents,
                    scores[i],
                ]
            )

    return data


def set_relevances(ctx, query, results):
    rf = RelevanceFeedback(ctx)
    for result in results:
        for relevances in rf.access(query):
            if result[1] == relevances[1]:
                result[0] = "relevant"
        if not result[0] == "relevant":
            result[0] = "not relevant"
    return results


# return a Context object with the user's selections
def construct_context(values):
    if values["_uottawa_"]:
        corpus_path = path.abspath("data/corpus/UofO_Courses.yaml")
        dictionary_path = path.abspath("data/dictionary/UofOCourses.txt")
        inverted_index_path = path.abspath("data/index/UofO_Courses.yaml")
    elif values["_reuters_"]:
        corpus_path = path.abspath("data/corpus/reuters.yaml")
        dictionary_path = path.abspath("data/dictionary/reuters.txt")
        inverted_index_path = path.abspath("data/index/reuters.yaml")

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


def mix_in(query, expansions, values):
    new_query = ""

    if values["_vsm_"]:
        new_query = query
        for terms in expansions.values():
            for term in terms:
                new_query += " " + term
    elif values["_boolean_"]:
        # definitely not fool-proof, trying to put synonyms in OR'd statements together
        for q in query.split(" "):
            if q in ["(", ")", "AND", "OR", "AND_NOT"] or q not in expansions:
                new_query += " " + q
            elif q in expansions:
                new_query += " (" + q
                for ex in expansions[q]:
                    new_query += " OR " + ex
                new_query += ")"

    return new_query


def rocchio(original_query, data):
    print("STUB")
