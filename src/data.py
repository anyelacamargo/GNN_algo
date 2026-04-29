import pandas as pd
from pykeen.triples import TriplesFactory


# =========================================================
# LOAD TRIPLES
# =========================================================
def load_triples(path):
    df = pd.read_csv(path, sep="\t", header=None)

    # standard KG format: head, tail, relation
    df.columns = ["head", "tail", "relation"]

    return df[["head", "relation", "tail"]]


# =========================================================
# BUILD TRIPLE FACTORIES (FIXED VERSION)
# =========================================================
def build_factories(train_df, valid_df, test_df):

    # -----------------------------------------------------
    # IMPORTANT FIX:
    # build mapping on ALL data to avoid dropping triples
    # -----------------------------------------------------
    all_df = pd.concat([train_df, valid_df, test_df], ignore_index=True)

    full_factory = TriplesFactory.from_labeled_triples(all_df.values)

    # reuse SAME global mapping for all splits
    training = TriplesFactory.from_labeled_triples(
        train_df.values,
        entity_to_id=full_factory.entity_to_id,
        relation_to_id=full_factory.relation_to_id,
    )

    validation = TriplesFactory.from_labeled_triples(
        valid_df.values,
        entity_to_id=full_factory.entity_to_id,
        relation_to_id=full_factory.relation_to_id,
    )

    testing = TriplesFactory.from_labeled_triples(
        test_df.values,
        entity_to_id=full_factory.entity_to_id,
        relation_to_id=full_factory.relation_to_id,
    )

    return training, validation, testing


# =========================================================
# LOAD DISEASE ENTITIES
# =========================================================
def load_disease_entities(path):
    disease_entities = set()

    with open(path, "r") as f:
        for line in f:
            entity, etype = line.strip().split("\t")
            if etype == "DISEASE":
                disease_entities.add(entity)

    return disease_entities