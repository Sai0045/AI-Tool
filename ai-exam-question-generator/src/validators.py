from .paper_schema import Paper

def validate_total_marks(paper: Paper) -> list[str]:
    errors = []
    calc = sum(q.marks for q in paper.questions)
    if calc != paper.total_marks:
        errors.append(f"Total marks mismatch: expected {paper.total_marks}, got {calc}")
    return errors

def validate_unit_coverage(paper: Paper, min_units: int = 2) -> list[str]:
    units = {q.unit for q in paper.questions}
    if len(units) < min_units:
        return [f"Low unit coverage: only {len(units)} unit(s) covered."]
    return []
