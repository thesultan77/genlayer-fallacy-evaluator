# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

class FallacyRegistry(gl.Contract):
    count: str
    record_0: str
    record_1: str
    record_2: str
    record_3: str
    record_4: str

    def __init__(self):
        self.count = "0"
        self.record_0 = ""
        self.record_1 = ""
        self.record_2 = ""
        self.record_3 = ""
        self.record_4 = ""

    @gl.public.write
    def submit_and_evaluate(self, argument_text: str) -> None:
        def nondet_eval() -> str:
            prompt = (
                "Task: Classify this argument for logical fallacies: '" + argument_text + "'\n"
                "Return exactly four fields separated by '|||':\n"
                "Field 1 (Fallacy Type): Formal Fallacy, Ad Hominem, Straw Man, False Dilemma, Slippery Slope, Circular Reasoning, Red Herring, Appeal to Authority, or None\n"
                "Field 2 (Validity): VALID or INVALID\n"
                "Field 3 (Severity): 0, 1, 2, 3, 4, or 5\n"
                "Field 4 (Summary): Brief explanation in one sentence\n"
                "Output format: <Fallacy>|||<Validity>|||<Severity>|||<Summary>"
            )
            return gl.nondet.llm(prompt)

        def check_equiv(a: str, b: str) -> bool:
            parts_a = a.split("|||")
            parts_b = b.split("|||")
            if len(parts_a) != 4 or len(parts_b) != 4:
                return False

            # Independently verify every core verdict field before committing
            fallacy_eq = parts_a[0].strip().lower() == parts_b[0].strip().lower()
            validity_eq = parts_a[1].strip().upper() == parts_b[1].strip().upper()
            severity_eq = parts_a[2].strip() == parts_b[2].strip()
            summary_present = len(parts_a[3].strip()) > 0 and len(parts_b[3].strip()) > 0

            return fallacy_eq and validity_eq and severity_eq and summary_present

        verdict = gl.eq_principle(nondet_eval, check_equiv)
        current_idx = int(self.count)
        entry = "Arg: " + argument_text + " => " + verdict

        if current_idx == 0:
            self.record_0 = entry
        elif current_idx == 1:
            self.record_1 = entry
        elif current_idx == 2:
            self.record_2 = entry
        elif current_idx == 3:
            self.record_3 = entry
        else:
            self.record_4 = entry

        self.count = str(current_idx + 1)

    @gl.public.view
    def get_evaluation(self, index: str) -> str:
        if index == "0":
            return self.record_0
        elif index == "1":
            return self.record_1
        elif index == "2":
            return self.record_2
        elif index == "3":
            return self.record_3
        elif index == "4":
            return self.record_4
        return "Record not found"

    @gl.public.view
    def get_total_count(self) -> str:
        return self.count
