import markdown
import panel as pn

from src.chatbot import ChatBot


def clear_input(event):
    """
    Function to clear the input text box.
    """
    input_question.value = ""


# Read the markdown file with specified encoding
with open("resume/resume.md", "r", encoding="utf-8") as f:
    md_string = f.read()

html = markdown.markdown(md_string)
panel_obj = pn.pane.Markdown(md_string, sizing_mode="stretch_width")

resume = pn.Column(
    panel_obj,
    sizing_mode="stretch_width",
)

disclaimer = pn.pane.Alert(
    """
    **Attention: This chatbot is powered by OpenAI's GPT-3.5, 
    one of the most advanced language models currently available. 
    Please be aware that while GPT-3.5 strives to provide accurate and relevant responses, 
    it can sometimes generate information that is not entirely correct or can 'hallucinate' 
    details that don't exist. 
    Always cross-check important information and use the chatbot responsibly.**   
    """,
    alert_type="danger",
    sizing_mode="stretch_width",
)

input_question = pn.widgets.TextInput(
    placeholder="Ask me a question here!!!",
    sizing_mode="stretch_width",
)

moe = ChatBot()
dialogue = pn.bind(moe.convchain, input_question)

moe.param.watch(clear_input, "answer")

conversation = pn.Column(
    "",
    pn.panel(dialogue, loading_indicator=True, sizing_mode="stretch_both"),
    pn.layout.Divider(),
    input_question,
)

chat_history = pn.Column(
    pn.panel(moe.get_chat_history, sizing_mode="stretch_width"),
    pn.layout.Divider(),
)

download_resume = pn.widgets.FileDownload(
    filename="resume/resume.md",
    button_type="primary",
)

example_question = pn.Column(
    "## Example Questions",
    pn.pane.Markdown(
        """
        - What are you looking for in your next role?
        - Are you a suitable candidate for Data Science?
        - What Data engineering projects you have done?
        - What is your experience with Python?
        - What is your experience with SQL?
        """
    ),
)

chatbot = pn.Column(
    "## Chat with my Resume",
    disclaimer,
    pn.layout.Divider(),
    pn.Tabs(
        ("Conversation", conversation),
        ("Chat History", chat_history),
        ("Example Questions", example_question),
        ("Download Resume", download_resume),
        sizing_mode="stretch_both",
    ),
    max_width=600,
    styles=dict(
        background="WhiteSmoke",
        padding="15px",
        border="1px solid black",
        position="sticky",
        top="10px",
    ),
)

layout = pn.Column(
    pn.Row(resume, chatbot),
)


template = pn.template.MaterialTemplate(
    title="Resume Chatbot",
    main=[layout],
)

template.servable()
