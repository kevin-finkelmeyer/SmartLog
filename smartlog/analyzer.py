import os
from pathlib import Path

from groq import Groq

from smartlog.parser import SmartLogParser


class Analyzer:
    def __init__(self, filename):
        self.client = Groq(api_key=os.environ['GROQ_API_KEY'])
        self.path = Path(filename)
        self.data = SmartLogParser(self.path).parse()
        self.data_str = ""

    def __analyze__(self):
        message_counts = self.data.groupby(['level', 'message']).size().reset_index(name='count')
        message_counts = message_counts.sort_values(['level', 'count'], ascending=[True, False])

        service_most_err = self.data[self.data['level'] == 'ERROR'].groupby(['service', 'level']).size()
        service_most_err = service_most_err.sort_values(ascending=[False])

        most_recent_err = self.data[(self.data['level'] == 'ERROR') | (self.data['level'] == 'CRITICAL')][-5:]

        least_common_messages = self.data.groupby(
            ['message']).size().reset_index(
            name='count').sort_values(
            ['count'],
            ascending=[
                True])[:5]

        self.data_str = (f"Messages grouped by their Level:\n{message_counts.to_string()}\n"
                         f"Service with most errors:\n{service_most_err.to_string()}\n"
                         f"The last 5 errors or criticals:\n{most_recent_err.to_string()}\n"
                         f"The least common messages:\n{least_common_messages.to_string()}\n")

    def __build_prompt__(self, system_context: str = None):
        prompt = f"CONTEXT: {system_context}\n\nDATA:{self.data_str}\n\n"
        return prompt

    def ask(self):
        self.__analyze__()
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Role: You are a Senior Site Reliability Engineer (SRE).\nObjective: Detect anomalies in the provided log data. Focus on patterns indicating system failures, performance bottlenecks, or security threats.\n"
                               "Context: Use provided system context. If missing, infer from log syntax (e.g., Cloud-Native, DB, Auth).\n"
                               "Input: You will receive summarized log frequencies (Level, Message, Count).\n"
                               "Constraints: Be extremely concise. No greetings. No filler text.\n\n"
                               "Output Format:\n"
                               "ANOMALY: [Brief description of the detected issue]\n\n"
                               "ROOT CAUSE: [Most likely technical reason]}\n\n"
                               "ACTION: [Precise steps to resolve or investigate]"
                },
                {
                    "role": "user",
                    "content": self.__build_prompt__(),
                }
            ],
            model="llama-3.1-8b-instant",
            max_tokens=250,
            temperature=0.1
        )
        print(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    analyzer = Analyzer("../data/sample.log")
    analyzer.ask()
