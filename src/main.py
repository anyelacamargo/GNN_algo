import os
from config import *
from data import load_triples, build_factories, load_disease_entities
from graph import build_graph, print_stats, plot_degree_distribution
from model import train_model, save_model, load_model
from evaluate import compare_models
from predict import predict_diseases


# ================================
# LOAD DATA
# ================================
print("\n[1] Loading data...")
train_df = load_triples(TRAIN_FILE)
valid_df = load_triples(VALID_FILE)
test_df  = load_triples(TEST_FILE)

training, validation, testing = build_factories(train_df, valid_df, test_df)


# ================================
# GRAPH EXPLORATION
# ================================
print("\n[2] Graph exploration...")
G = build_graph(train_df)
print_stats(G)
plot_degree_distribution(G)


# ================================
# TRAIN OR LOAD MODELS
# ================================
print("\n[3] Train or load models...")

results = {}
models = {}

for model_name in MODELS:

    model_path = f"models/{model_name}.pkl"

    if os.path.exists(model_path):
        print(f" Loading existing {model_name}")
        result = load_model(model_name)

    else:
        print(f" Training {model_name}")
        result = train_model(model_name, training, validation, testing)
        save_model(result, model_name)

    results[model_name] = result
    models[model_name] = result.model


# ================================
# EVALUATION (ONLY IF TRAINED)
# ================================
print("\n[4] Model evaluation...")

if results:  # only if we trained in this run

    results_table = compare_models(results)

    print("\n=== MODEL COMPARISON ===")
    print(results_table)

    best_model_name = results_table.loc[
        results_table["MRR"].idxmax(), "model"
    ]

else:
    print("No new training performed → skipping evaluation")

    # fallback: choose a default model
    best_model_name = MODELS[-1]  # e.g. ComplEx


best_model = models[best_model_name]

print(f"\nSelected model: {best_model_name}")


# ================================
# PREDICTION
# ================================
print("\n[5] Running predictions...")

genes = ["PHYHIPL", "TTC9", "BRCA1"]
disease_entities = load_disease_entities("data/entity2type.txt")

preds = predict_diseases(
    model=best_model,
    tf=training,
    gene_list=genes,
    relation="GENE_DISEASE_ot_genetic_association",
    disease_entities=disease_entities
)


for gene, df in preds.items():
    print(f"\nTop diseases for {gene}:")
    print(df)


# ================================
# DONE
# ================================
print("\nPipeline completed successfully.")
