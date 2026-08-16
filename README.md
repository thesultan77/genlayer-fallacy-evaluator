# AI Logical Fallacy & Argument Evaluator

An Intelligent Contract built on **GenLayer** that utilizes decentralized LLM execution and the **Equivalence Principle** consensus mechanism to evaluate arguments for logical fallacies, soundness, and validity.

---

## 📌 Overview

Traditional smart contracts are deterministic and cannot evaluate nuanced natural language arguments. This Intelligent Contract uses GenLayer's non-deterministic execution layer (`gl.nondet.llm`) to inspect text for common formal and informal logical fallacies (such as *Ad Hominem*, *Straw Man*, *False Dilemma*, and *Circular Reasoning*).

Validator consensus is achieved via `gl.eq_principle`, ensuring that multiple validator nodes agree semantically on the analysis before committing the verdict to the blockchain state.

---

## ⚙️ How It Works

1. **Non-Deterministic Evaluation (`nondet_eval`):**
   - The contract feeds the user-submitted argument into an LLM with structured evaluation prompts.
2. **Equivalence Principle Consensus (`check_equiv`):**
   - Different validators query LLMs independently.
   - The contract uses a semantic equivalence checker (`check_equiv`) to verify if the LLM responses agree on the core fallacy findings and validity.
3. **On-Chain State Update:**
   - Once consensus is reached, the argument and its verified verdict are stored in contract storage.

---

## 📜 Contract Interface

### Methods

* **`evaluate_argument(argument_text: str) -> None`** *(Write Method)*  
  Submits an argument for decentralized LLM fallacy analysis and consensus verification.
* **`get_last_verdict() -> str`** *(View Method)*  
  Retrieves the latest evaluated argument verdict stored on-chain.

---

## 🚀 Deployment & Testing

* **Studio Contract Address:** `0x5E4Fb9acd56B282115671516BC26aD889DF620C8`
* **Network:** GenLayer Studio Testnet
* **Framework:** `py-genlayer` (v0.2.16)

### Sample Test Inputs

* **Input 1 (Appeal to Popularity / Bandwagon):**
  > `"Everyone is buying this asset right now, so it must be completely safe."`
  > **Expected Result:** Flagged as *Bandwagon Fallacy / Argumentum ad Populum*.

* **Input 2 (Ad Hominem):**
  > `"You cannot trust his economic plan because he has never run a corporation."`
  > **Expected Result:** Flagged as *Ad Hominem*.
