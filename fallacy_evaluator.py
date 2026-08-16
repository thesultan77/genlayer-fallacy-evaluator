# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

class ArgumentEvaluator(gl.Contract):
    last_argument: str
    last_verdict: str

    def __init__(self):
        self.last_argument = ""
        self.last_verdict = ""

    @gl.public.write
    def evaluate_argument(self, argument_text: str) -> None:
        def nondet_eval() -> str:
            prompt = "Analyze if this argument has fallacies: " + argument_text
            return gl.nondet.llm(prompt)

        def check_equiv(a: str, b: str) -> bool:
            prompt = "Do these two evaluations agree? 1: " + a + " 2: " + b + ". Output YES or NO."
            return gl.nondet.llm(prompt).strip().upper() == "YES"

        verdict = gl.eq_principle(nondet_eval, check_equiv)
        self.last_argument = argument_text
        self.last_verdict = verdict

    @gl.public.view
    def get_last_verdict(self) -> str:
        return self.last_verdict
