# Knowledge Graph Completion for Gene–Disease Prediction

Anyela Camargo
## Overview
This project reconstructs a knowledge graph embedding (KGE) pipeline to predict gene–disease associations via link prediction.

We model relationships of the form:

(GENE) - [GENE_DISEASE_ot_genetic_association] ->(DISEASE)

## Project Structure

```
root/
├── data/        # train / valid / test triples
├── models/      # saved model checkpoints
├── src/         # pipeline modules
│   ├── main.py
│   ├── model.py
│   ├── data.py
│   ├── evaluate.py
│   ├── predict.py
│   └── ...
├── requirements.txt
├── Dockerfile
├── README.md
├── GNN_algo.R
├── run.sh
└── run.bat
```


## pre-training, data QC, data features:
Run the R script GNN_algo.R to analyse the graph

- Very large, almost fully connected graph (≈99.8% in one component)
- Highly skewed degree distribution with extreme in-degree hubs (max 8113, median 0)
- Low average connectivity (~3 edges/node) but strong hub dominance
- Only 4 relations with low diversity (entropy ≈ 1.35)
- Fully directed structure with no reciprocal edges
- Strong asymmetry in connectivity (many more asymmetric than mutual dyads)
- Betweenness is extremely skewed, with a few nodes dominating graph flow
- Overall: hub-heavy, low-relation, highly imbalanced directed KG

### Model Comparison

| Model     | Handles Asymmetry | Best For                        | Expected Behaviour on This Dataset | Why it Matters Here |
|-----------|------------------|--------------------------------|------------------------------------|---------------------|
| TransE    | Limited          | Simple translational patterns  | Fast baseline, weaker ranking      | Struggles with many-to-one mappings (genes-> diseases) |
| DistMult  | No               | Symmetric relations            | Poor fit                          | Cannot model directionality in gene–disease links |
| ComplEx   | Yes              | Asymmetric + multi-relational graphs | Strong performance | Captures directional gene -> disease relationships |
| RotatE    | Yes              | Complex relational patterns     | Potentially strong but slower      | Could model hierarchical biological structure |


Three models are trained and compared:
- DistMult: not attemped
- TransE: simple and fast baseline
- ComplEx: models asymmetric relations (better suited for this task)
- RotatE: models asymmetric relations and better suited for the graph topology. It handles direction and rotation structure
---

## How to Run

### Linux simple
./run.sh

### Windows
./run.bat


### Docker (recommended)

docker build -t kg-pipeline .
docker run kg-pipeline

GPU:

docker run --gpus all kg-pipeline

Persist models and data:

docker run --gpus all \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  kg-pipeline

---

### Local Python

pip install -r requirements.txt
python src/main.py

---
### Colab

GNN_algo


## Pipeline

1. Load triples and build entity/relation mappings
2. Explore graph structure (degree distribution, connectivity)
3. Train models (TransE, ComplEx, RotatE)
4. Evaluate using:
   - MRR
   - Hits@10
   - Head vs Tail metrics
5. Select best model based on MRR
6. Predict diseases from genes

---

## Model Persistence

Models are saved in:

models/{model}.pkl

If file exists:
- model is loaded
- retraining is skipped

---


## Reproducibility

- Fixed random seed
- Consistent dataset splits
- Dependency management via requirements.txt
- Optional Docker environment

---

## Example

GENE: BRCA1
RELATION: GENE_DISEASE_ot_genetic_association

Output:
Top predicted diseases ranked by score

---


## Model Specification (Data-Aware Design)

The choice of knowledge graph embedding models is guided by the structure of the dataset:

- Entities: Genes, Diseases, Variants
- Relations: Mostly directed biological associations
- Task: Link prediction (Gene -> Disease)

The graph is highly **asymmetric and hub-structured**, where:
- Genes are low-degree, specific entities
- Diseases are high-degree, shared targets across many genes

### Parameters to optimise

- Epochs = [1, 50, 100, 200, 300, 400]
- negatives = [5,10, 20]
- embeddings = [200, 400]
- processor = [CPU, GPU]
- Data: Filtering Train (Y/N)
- Test: [1,5,200, CPU, N]
- Best: [300, 10, 200, GPU, N]


### Dataset Implications

- High-degree disease nodes -> ranking task is difficult
- Many-to-one relations (genes-> diseases) -> requires asymmetric modeling
- Sparse gene connectivity -> embedding quality depends on relation modeling more than node frequency

###Results


[4] Model evaluation...

=== MODEL COMPARISON ===
     model       MRR   Hits@10  MRR_head  Hits@10_head  MRR_tail  Hits@10_tail
0   TransE  0.025959  0.053170  0.004750      0.008178  0.047169      0.098162
1  ComplEx  0.005933  0.012223  0.001021      0.001543  0.010844      0.022904

Selected model: TransE

[5] Running predictions...

Top diseases for PHYHIPL:
                                               tail_label     score
133245        susceptibility_to_scarlet_fever_measurement -7.845275
38008                         peripheral_arterial_disease -7.905086
12      3-hydroxy-1-methylpropylmercapturic_acid_measu... -8.036821
37077                                 atrial_fibrillation -8.043812
23974                                         QT_interval -8.052061
37350                                endometrial_neoplasm -8.137326
37102          behavioural_inhibitory_control_measurement -8.148748
37081                       atrophic_macular_degeneration -8.192574
37743                                      morbid_obesity -8.226606
37624                        late-onset_myasthenia_gravis -8.238958

Top diseases for TTC9:
                              tail_label     score
30965                        Renal_Colic -9.292908
38081                           pulpitis -9.432117
37089              autonomic_dysreflexia -9.464842
38266                     rhabdomyolysis -9.479968
37671                           lymphoma -9.535545
37979  overweight_body_mass_index_status -9.653752
37259           congestive_heart_failure -9.662451
30967                         Renal_cyst -9.670377
37966                         osteopenia -9.699081
37743                     morbid_obesity -9.709112

Top diseases for BRCA1:
                                tail_label     score
37480                         hearing_loss -8.972750
37653                            longevity -9.031398
37309                           diphtheria -9.091722
11755                Dupuytren_Contracture -9.113667
37671                             lymphoma -9.123935
37270   cups_of_coffee_per_day_measurement -9.208780
37116         body_composition_measurement -9.222947
133221                              suntan -9.262373
37635                             leukemia -9.266050
38178           response_to_glucocorticoid -9.279806



] Model evaluation...

=== MODEL COMPARISON ===
     model       MRR   Hits@10  MRR_head  Hits@10_head  MRR_tail  Hits@10_tail
0  ComplEx  0.006822  0.015226  0.000829      0.001064  0.012814      0.029389
1   RotatE  0.135851  0.193847  0.048127      0.078009  0.223574      0.309686

Selected model: RotatE

[5] Running predictions...

Top diseases for PHYHIPL:
                            tail_label     score
1608        lip_morphology_measurement -3.098593
1482  Trypanosoma_cruzi_seropositivity -3.129549
2485        nighttime_rest_measurement -3.139509
533                        QT_interval -3.153296
3231         linoleic_acid_measurement -3.248063
4213                       PR_interval -3.360635
51                        QRS_duration -3.402052
1159         type_II_diabetes_mellitus -3.548495
325           response_to_sulfonylurea -3.569845
915                       age_at_onset -3.574582

Top diseases for TTC9:
                        tail_label     score
200                  schizophrenia -3.980365
2368                        asthma -4.000517
4472                        sepsis -4.003740
3551      type_I_diabetes_mellitus -4.022127
2723     colorectal_adenocarcinoma -4.035750
3437  systemic_lupus_erythematosus -4.040487
2813  chronic_lymphocytic_leukemia -4.042240
264      blood_protein_measurement -4.054511
3043      response_to_paliperidone -4.059730
3381              multiple_myeloma -4.069625

Top diseases for BRCA1:
                                  tail_label     score
4655                        rhabdomyosarcoma -3.172443
3657                myelodysplastic_syndrome -3.183449
2461                   ductal_adenocarcinoma -3.211095
4330                  acute_myeloid_leukemia -3.212977
2195              invasive_lobular_carcinoma -3.236111
4482                       ovarian_carcinoma -3.236120
515                     pancreatic_carcinoma -3.285087
2712  Fanconi_anemia_complementation_group_A -3.293446
2723               colorectal_adenocarcinoma -3.294321
2813            chronic_lymphocytic_leukemia -3.300998



## Other Specs
```text
## epochs=100, negatives=25, emb=400
=== MODEL COMPARISON ===
model     MRR       Hits@10  MRR_head  Hits@10_head  MRR_tail  Hits@10_tail
TransE    0.025959  0.053170 0.004750  0.008178      0.047169  0.098162
ComplEx   0.005933  0.012223 0.001021  0.001543      0.010844  0.022904


## epochs=400, negatives=5, emb=200
=== MODEL COMPARISON ===
model     MRR       Hits@10  MRR_head  Hits@10_head  MRR_tail  Hits@10_tail
RotatE    0.150642  0.220155 0.066549  0.107156      0.234734  0.333153

Selected model: RotatE


## epochs=200, negatives=20, emb=200
=== MODEL COMPARISON ===
model     MRR       Hits@10  MRR_head  Hits@10_head  MRR_tail  Hits@10_tail
RotatE    0.148295  0.213139 0.064395  0.101174      0.232196  ...


## epochs=100, negatives=20, emb=200
=== MODEL COMPARISON ===
     model       MRR   Hits@10  MRR_head  Hits@10_head  MRR_tail  Hits@10_tail
0  ComplEx  0.006822  0.015226  0.000829      0.001064  0.012814      0.029389
1   RotatE  0.135851  0.193847  0.048127      0.078009  0.223574      0.309686
```



