from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall
from app.services.rag_chain import get_rag_chain

TEST_CASES = [
    {"question": "Summarise the key points.", "ground_truth": "Depends on your documents."},
]

def build_eval_dataset():
    chain = get_rag_chain()
    rows  = []
    for tc in TEST_CASES:
        result = chain.invoke({"query": tc["question"]})
        rows.append({
            "question":     tc["question"],
            "answer":       result["result"],
            "contexts":     [d.page_content for d in result["source_documents"]],
            "ground_truth": tc["ground_truth"],
        })
    return Dataset.from_list(rows)

if __name__ == "__main__":
    dataset = build_eval_dataset()
    results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_recall])
    print(results.to_pandas().to_string())