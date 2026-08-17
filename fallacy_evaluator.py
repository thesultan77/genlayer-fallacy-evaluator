# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

class ArgumentEvaluator(gl.Contract):
    last_argument: str
    fallacy_name: str
    is_valid: str
    severity: str
    analysis: str

    def __init__(self):
        self.last_argument = ""
        self.fallacy_name = "None"
        self.is_valid = "Valid"
        self.severity = "0"
        self.analysis = ""

    @gl.public.write
    def evaluate_argument(self, argument_text: str) -> None:
        def nondet_eval() -> str:
            prompt = (
                "Analyze this argument for logical fallacies: '" + argument_text + "'. "
                "Format output exactly as 4 lines separated by semicolons: "
                "FALLACY: <name or None>; VALIDITY: <Valid or Invalid>; SEVERITY: <0-5>; ANALYSIS: <short reason>"
            )
            return gl.nondet.llm(prompt)

        def check_equiv(a: str, b: str) -> bool:
            parts_a = a.split(";")
            parts_b = b.split(";")
            if len(parts_a) >= 2 and len(parts_b) >= 2:
                fallacy_match = parts_a[0].strip().lower() == parts_b[0].strip().lower()
                validity_match = parts_a[1].strip().lower() == parts_b[1].strip().lower()
                return fallacy_match and validity_match
            return False

        verdict = gl.eq_principle(nondet_eval, check_equiv)
        parts = verdict.split(";")

        self.last_argument = argument_text
        if len(parts) >= 4:
            self.fallacy_name = parts[0].strip()
            self.is_valid = parts[1].strip()
            self.severity = parts[2].strip()
            self.analysis = parts[3].strip()
        else:
            self.fallacy_name = "Evaluated"
            self.is_valid = "Determined"
            self.severity = "1"
            self.analysis = verdict

    @gl.public.view
    def get_last_verdict(self) -> str:
        return (
            "Argument: " + self.last_argument + " | " +
            self.fallacy_name + " | " +
            self.is_valid + " | " +
            self.severity + " | " +
            self.analysis
        )
