from groq import Groq
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class ChatEngine:
    """
    Feeds EDA summary as context to Groq-hosted Llama model
    &
    handles natural language Q&A on the uploaded dataset.
    """
    def __init__(self,
                 numeric_summary: pd.DataFrame,
                 categorical_summary: pd.DataFrame,
                 model: str = "llama-3.3-70b-versatile"):
        """
        Args:
             numeric_summary: Numeric stats DataFrame from EDAEngine.
             categorical_summary: Categorical stats DataFrame from EDAEngine.
             model: Ollama model name
        """
        self.numeric_summary = numeric_summary
        self.categorical_summary = categorical_summary
        self.model = model
        self.messages = []
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _build_system_prompt(self) -> str:
        """
        Converts EDA summaries to plain text and builds the system prompt.
        &
        Restrict the LLM to only answer dataset-related questions.

        Returns:
            str: The formatted system prompt.
        """
        numeric_text = self.numeric_summary.to_string()
        categorical_text = self.categorical_summary.to_string()

        prompt = f"""
                You are an expert data analyst assistant.
                You have been given the following statistical summary of an uploaded dataset.

                NUMERIC SUMMARY:
                {numeric_text}

                CATEGORICAL SUMMARY:
                {categorical_text}

                Your job is to answer questions about this dataset clearly and concisely.
                Only answer questions related to this dataset.
                If the user asks anything unrelated, politely decline and redirect them.
                """
        return prompt

    def chat(self, user_question: str) -> str:
        """
        Sends user question to Ollama with EDA knowledge and returns the response.

        Args:
            user_question: The question typed by the user.

        Returns:
            str: The LLM's response text.
        """
        # Inject system prompt only on the first message
        if len(self.messages) == 0:
            self.messages.append({
                "role": "system",
                "content": self._build_system_prompt()
            })

        # Append the user's question
        self.messages.append({
            "role": "user",
            "content": user_question
        })

        # Call Ollama
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )

        # Extract response text
        reply = response.choices[0].message.content

        # Append assistant reply to maintain conversation history
        self.messages.append({
            "role": "assistant",
            "content": reply
        })

        return reply
