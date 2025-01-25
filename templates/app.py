from flask import Flask, render_template, request
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()


def llm(prompt, submission):
    client = AzureOpenAI(
        api_key=os.getenv("GPT_API_KEY"),
        api_version="2023-05-15",
        azure_endpoint="https://api.umgpt.umich.edu/azure-openai-api",
        organization=os.getenv("SHORTCODE"),
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": submission},
        ],
        temperature=.5,
        stop=None,
    )
    return response.choices[0].message.content

# Load rubric from file


def load_rubric():
    with open("rubric.txt", "r") as file:
        return file.read()

# Home page to submit an essay


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        essay = request.form["essay"]
        rubric = load_rubric()
        prompt = f"As an AI system integrated with GradeSupport, your main role is to assist students in self-assessing their assignments by utilizing UM Maizey's capabilities. You are tasked with analyzing student submissions against the provided assignment rubrics. Your steps should include: 1) Evaluate each criterion of the rubric and assign a score out of 10 for each criteria. 2) Offer constructive and actionable feedback to help students improve their work. 3) Always guide students towards finding the correct answer on their own, rather than providing direct answers. Ensure your feedback is clear, supportive, and focused on enhancing their learning experience:\n\n{rubric}"
        grade = llm(prompt, essay)
        return render_template("results.html", grade=grade)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
