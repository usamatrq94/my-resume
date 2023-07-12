import panel as pn
import param

from src.db_chains import load_resume


class ChatBot(param.Parameterized):
    chat_history = param.List([])
    answer = param.String("")

    def __init__(self, **params):
        super(ChatBot, self).__init__(**params)
        self.panels = []
        self.resume = load_resume()

    def convchain(self, question: str):
        """
        This method is called when the user asks a question.
        """
        if not question:
            return pn.WidgetBox(
                pn.Row(
                    "Enter your question below:",
                    pn.pane.Markdown(""),
                    max_width=400,
                    sizing_mode="stretch_width",
                ),
                scroll=False,
            )

        answer = self.resume({"question": question, "chat_history": self.chat_history})

        self.chat_history.extend([question, answer["answer"]])
        self.answer = answer["answer"]

        self.panels.extend(
            [
                pn.Row(
                    "Question:",
                    pn.pane.Markdown(question),
                    max_width=450,
                    sizing_mode="stretch_width",
                ),
                pn.Row(
                    "Response:",
                    pn.pane.Markdown(
                        self.answer,
                    ),
                    max_width=450,
                    sizing_mode="stretch_width",
                ),
            ]
        )

        return pn.WidgetBox(*self.panels)

    @param.depends("convchain")
    def get_chat_history(self):
        """
        This method is called when the user wants to see the chat history.
        """
        if not self.chat_history:
            return pn.WidgetBox(
                pn.Row(
                    pn.pane.Str("No chat history yet"),
                    max_width=400,
                    sizing_mode="stretch_width",
                )
            )

        return_list = [
            pn.Row(
                pn.pane.Markdown(
                    "Current Chat History", styles={"background-color": "#F6F6F6"}
                )
            )
        ]

        for exchange in self.chat_history:
            return_list.append(
                pn.Row(
                    pn.pane.Str(exchange),
                )
            )
        return pn.WidgetBox(*return_list)
