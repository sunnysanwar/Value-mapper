import gradio as gr
from src.helper import get_keywords
from src.const import FILENAME, MODEL
from utils.fuzzy import find_matching_keywords
from utils.gpt import gpt_suggest_keywords, create_embedding

KEYWORDS = get_keywords(FILENAME)
KEYWORDS_EMBEDDING = create_embedding(KEYWORDS)
def matching_keywords(keyword, select_model):
    if select_model == MODEL[0]:
        keywords = find_matching_keywords(keyword, KEYWORDS)
    else:
        keywords = gpt_suggest_keywords(keyword, KEYWORDS, KEYWORDS_EMBEDDING)
    if keywords:
        return gr.Dropdown(choices=keywords, value=keywords[0], interactive=True, visible=True), gr.JSON(visible=True), {"keyword": keyword, "similar keywords": keywords}
    else:
        return gr.Dropdown(visible=True, interactive=False), gr.JSON(visible=False), None


def GUI():
    with gr.Blocks() as system_ui:
        gr.Markdown('''
                    <center>
                        <h1> Keywords Matching Suggestion System </h1>
                    </center>
                    ''')
        system_ui.title = "keywords_system"
        user_input = gr.Textbox(label="Input")
        select_model = gr.Radio(choices=MODEL, label="Select the model", value=MODEL[0], interactive=True)
        model_output = gr.Dropdown(label="Suggest Keywords", visible=True, interactive=False)
        json_output = gr.JSON(label="Keywords", visible=False)
        user_input.submit(matching_keywords, inputs=[user_input, select_model], outputs=[model_output, json_output, json_output])
    return system_ui
