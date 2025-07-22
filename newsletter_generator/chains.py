from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from .shemas.enums import PromptName
from .shemas.base import SummaryModel, PromptTemplate
from string import Template
from django.conf import settings
import yaml
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(settings.BASE_DIR, ".env.local")
load_dotenv(dotenv_path)

prompt_path = os.path.join(
    settings.BASE_DIR, "newsletter_generator", "shemas", "prompts_templates.yaml"
)
newsletter_template_path = os.path.join(
    settings.BASE_DIR, "newsletter_generator", "shemas", "newsletter_template.html"
)

with open(prompt_path, "r", encoding="utf-8") as file:
    templates = yaml.safe_load(file)

with open(newsletter_template_path, "r", encoding="utf-8") as file:
    newsletter_template = file.read()


def get_template(name):
    if name in templates:
        return PromptTemplate(**templates[name])
    else:
        raise ValueError(f"Template '{name}' not found in prompts_templates.yaml")


class Chain:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o")
        self.prompt = get_template(PromptName.edit_blog_post)
        self.edit_blog_post_chain = (
            ChatPromptTemplate.from_messages(
                [
                    ("system", self.prompt.system_message),
                    ("human", self.prompt.human_message),
                ]
            )
            | self.llm
            | PydanticOutputParser(pydantic_object=SummaryModel)
        )
        self.edit_blog_post_chain.name = "edit_blog_post_chain"

    def run(self, blog_post: str, url: str = None) -> str:
        inputs = {"blog_post": blog_post}
        output = self.edit_blog_post_chain.invoke(inputs)
        # output = SummaryModel(
        # Title="The Importance of Learning Python for Data Science",
        # Summary="Python is a versatile programming language that has become the de facto standard for data science. Its simplicity and readability make it accessible for beginners, while its powerful libraries like Pandas, NumPy, and Matplotlib provide advanced capabilities for data manipulation and visualization.",
        # Why_this_is_important="Python's extensive libraries and community support make it an essential tool for data scientists, enabling them to efficiently analyze and visualize data, build machine learning models, and automate tasks."
        # )
        html_content = Template(newsletter_template).substitute(
            blog_title=output.Title,
            article_summary=output.Summary,
            why_important=output.Why_this_is_important,
            url=url,
        )
        return html_content


example_input = """
Write a blog post about the importance of learning Python for data science.
"""

if __name__ == "__main__":
    chain = Chain()
    output_data = chain.edit_blog_post_chain.invoke({"blog_post": example_input.strip()})
    # output_data = SummaryModel(
    #     Title="The Importance of Learning Python for Data Science",
    #     Summary="Python is a versatile programming language that has become the de facto standard for data science. Its simplicity and readability make it accessible for beginners, while its powerful libraries like Pandas, NumPy, and Matplotlib provide advanced capabilities for data manipulation and visualization.",
    #     Why_this_is_important="Python's extensive libraries and community support make it an essential tool for data scientists, enabling them to efficiently analyze and visualize data, build machine learning models, and automate tasks.",
    # )
    print(output_data.Title)
    html_content = Template(newsletter_template).substitute(
        blog_title=output_data.Title,
        article_summary=output_data.Summary,
        why_important=output_data.Why_this_is_important,
        url="https://example.com/full-article-url",
    )
    print(html_content)
