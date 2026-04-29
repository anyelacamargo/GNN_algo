import torch
import pandas as pd




def predict_diseases(model, tf, gene_list, relation, disease_entities, top_k=10):
    """
    Predict diseases. Get a gene name and make predictions based on model
    : param model: model nama 
    : param gene_list: gene list to make predictions on
    : param relation: type of relation
    : param disease_entities: disease entities
    : param top_k: restrict results to k
    """


    outputs = {}

    device = next(model.parameters()).device
    relation_id = tf.relation_to_id[relation]

    # build mappings once
    id_to_entity = {v: k for k, v in tf.entity_to_id.items()}

    # 🔥 restrict candidate space FIRST
    disease_ids = [
        tf.entity_to_id[e]
        for e in disease_entities
        if e in tf.entity_to_id
    ]

    for gene in gene_list:

        if gene not in tf.entity_to_id:
            print(f"[SKIP] {gene}")
            continue

        head_id = tf.entity_to_id[gene]

        hr_batch = torch.tensor([[head_id, relation_id]], device=device)

        # score all, but slice immediately
        scores = model.predict_t(hr_batch).squeeze(0)

        scores = scores[disease_ids]

        df = pd.DataFrame({
            "tail_id": disease_ids,
            "score": scores.detach().cpu().numpy()
        })

        df["tail_label"] = df["tail_id"].map(id_to_entity)

        df = df.sort_values("score", ascending=False)

        outputs[gene] = df.head(top_k)[["tail_label", "score"]]

    return outputs
