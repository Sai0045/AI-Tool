from .paper_schema import Paper
import json

def export_markdown_paper(paper: Paper) -> str:
    md = []
    md.append(f"# {paper.title}")
    md.append(f"**Total Marks:** {paper.total_marks}\n")

    if paper.instructions:
        md.append("## Instructions")
        for ins in paper.instructions:
            md.append(f"- {ins}")
        md.append("")

    md.append("## Questions")
    for i, q in enumerate(paper.questions, start=1):
        md.append(f"**Q{i}. ({q.marks} marks) [{q.unit}] [{q.bloom_level}]**")
        md.append(f"- {q.question}")
        md.append("")
    return "\n".join(md)

def export_markdown_marking(paper: Paper) -> str:
    md = []
    md.append(f"# Marking Scheme: {paper.title}\n")
    for i, q in enumerate(paper.questions, start=1):
        md.append(f"## Q{i}. ({q.marks} marks) - {q.topic}")
        md.append("**Model Answer (points):**")
        for p in q.model_answer:
            md.append(f"- {p}")
        md.append("\n**Marking Breakdown:**")
        for m in q.marking_scheme:
            md.append(f"- {m}")
        md.append("")
    return "\n".join(md)

def export_json(paper: Paper) -> str:
    return paper.model_dump_json(indent=2)

def save_outputs(paper: Paper, outdir: str = "outputs") -> None:
    import os
    os.makedirs(outdir, exist_ok=True)

    with open(f"{outdir}/generated_paper.json", "w", encoding="utf-8") as f:
        f.write(export_json(paper))

    with open(f"{outdir}/question_paper.md", "w", encoding="utf-8") as f:
        f.write(export_markdown_paper(paper))

    with open(f"{outdir}/marking_scheme.md", "w", encoding="utf-8") as f:
        f.write(export_markdown_marking(paper))
