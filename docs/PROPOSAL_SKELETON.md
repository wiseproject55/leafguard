# LeafGuard Capstone Proposal Skeleton

Contents follow the **exact sequence** mandated on Slide 11 of the OUK guidelines.
Fill bracketed sections; do not reorder.

## Front Matter & Overview
1. **Title of the Project** — LeafGuard: AI-Based Crop Disease Detection and Treatment Advisory Web Platform
2. **Approval of Capstone/Mini Project** — [signature block: student(s), internal supervisor, industry mentor]
3. **Index** — [generated table of contents]
4. **Acknowledgment** — [supervisor, mentor, institution]
5. **Group Details & Contributions** — [member names, registration numbers, per-member task split]

## Introduction & Objective
- Problem: crop disease causes yield loss; expert diagnosis is scarce in rural areas.
- Objective: accessible web tool that classifies leaf disease from a photo and returns treatment advisory.
- Scope: [crops covered], image classification only (not in-field IoT sensing in v1).
- Outcomes: deployed web platform + trained model + evaluation.

## Technical Content

### Analysis (Feasibility, DFD, ER Diagrams)
- **Feasibility:** technical (open dataset PlantVillage, pretrained EfficientNet), economic (open-source stack), operational (web access).
- **DFD:** [Level-0: User → Upload → Inference → Advisory → Response. Level-1: expand auth, persistence, feedback.]
- **ER Diagram:** Users 1—N Diagnoses; Crops 1—N Diseases; Diseases 1—N Treatments; Diagnoses 1—1 Feedback. (Matches `app/models/entities.py`.)

### Hardware & Software Requirements
- Software: Python 3.11, Node 20, PostgreSQL 16, Docker. Libraries per `backend/requirements.txt` and `frontend/package.json`.
- Hardware (training): GPU recommended; CPU sufficient for inference. (Development hardware: [specify].)

### Tables, Structures, Modules, Data Structure
- Tables: users, crops, diseases, treatments, diagnoses, feedback.
- Modules: auth, diagnosis/inference, catalog, training, evaluation.

### Proposed System (Functional & Non-functional requirements, Methodology)
- **Functional:** see `docs/FUNCTIONALITIES.md` (14 items).
- **Non-functional:** prediction latency target, image size limit (8 MB), input validation, JWT security.
- **Methodology:** iterative/agile; transfer learning for the model; weekly supervisor + 3-weekly mentor checkpoints (per guidelines).

### Module Split-up & Gantt Chart
- [Map the 14 functionalities to a Week 4 → Week 15 timeline. Mark Week 15 = final product + report + oral presentation per Slide 9.]

## References & Cost Analysis
- References: PlantVillage dataset; EfficientNet (Tan & Le, 2019); FastAPI, PyTorch, React documentation. [Use full citations in the report.]
- Cost analysis: open-source stack (no license cost); hosting/compute estimate [specify]; GPU training time [specify].

---

## Mapping to Final Report Structure (Slide 12, 40–100 pages, Ch 1–7)

| Chapter | Source material already in repo |
|---------|--------------------------------|
| Ch 1 Introduction | this proposal's Introduction & Objective |
| Ch 2 Background | literature review + PlantVillage / prior CNN crop-disease work |
| Ch 3 Specification & Design | ER diagram (entities.py), DFD, use cases, UML |
| Ch 4 Implementation | backend/frontend/ml code, critical segments, challenges |
| Ch 5 Results & Evaluation | output of `ml/training/evaluate.py` (overall + per-class accuracy) |
| Ch 6 Future Work | enhancements list in `docs/FUNCTIONALITIES.md` |
| Ch 7 Conclusions | summary of findings |

## Compliance checklist (from Slides 9–10)
- [ ] Minimum 10–12 functionalities — **14 implemented**
- [ ] Version control (GitHub) — repo + CI present
- [ ] Deployment — docker-compose (db + api + web)
- [ ] Not inventory / CRUD-only / single-database — AI classifier + 6 related tables
- [ ] Proposal approved before implementation
- [ ] Project Progress Journal maintained (weekly supervisor, 3-weekly mentor)
- [ ] Final product + report + oral presentation due **beginning of Week 15**
