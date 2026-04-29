import os
from pykeen.pipeline import pipeline
from config import DEVICE, EPOCHS, LR
import pickle
from pykeen.pipeline import pipeline
from config import DEVICE, EPOCHS, LR



def train_model(model_name, training, validation, testing):
    """
    Train model
    : param model_name: model name e.g. "RotatE"
    : param training: training set
    : param test: test set
    : param validation: validation
    """

    print(f"[INFO] Training {model_name} on {DEVICE}")

    if model_name == "RotatE":
        embedding_dim = 200
        lr = 1e-4
        model_kwargs = dict(
            embedding_dim=embedding_dim
        )

    elif model_name == "ComplEx":
        embedding_dim = 200
        lr = 5e-4
        model_kwargs = dict(
            embedding_dim=embedding_dim,
        )

    else:  # TransE
        embedding_dim = 200
        lr = 5e-4
        model_kwargs = dict(
            embedding_dim=embedding_dim,
        )

    result = pipeline(
        training=training,
        validation=validation,
        testing=testing,

        model=model_name,
        device=DEVICE,

        model_kwargs=model_kwargs,

        training_kwargs=dict(
            num_epochs=EPOCHS,
            batch_size=1024,
        ),

        optimizer_kwargs=dict(
            lr=lr,
        ),

        negative_sampler="bernoulli",
        negative_sampler_kwargs=dict(
            num_negs_per_pos=50,
        ),

        evaluator_kwargs=dict(
            filtered=True,
        ),

        random_seed=42,
    )

    return result


def save_model(result, model_name, path="models"):
    """
    Save model
    : param result: results from train model
    : param model_name: model name
    : param model_name: model name
    : param path: path to save model
    """

    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, f"{model_name}.pkl")

    with open(file_path, "wb") as f:
        pickle.dump(result, f)

    print(f"[INFO] Saved full pipeline object to {file_path}")



def load_model(model_name, path="models"):
    """
    Load model
    : param model_name: model name
    : param path: path to save model
    """

    file_path = os.path.join(path, f"{model_name}.pkl")

    print(f"[INFO] Loading model from {file_path}")

    with open(file_path, "rb") as f:
        result = pickle.load(f)

    return result

def get_model(result):
    """
    Get model
    : param result: results from train model
    """

    return result.model


def predict_tail(model, triples_factory, head, relation, top_k=10):
    """
    Predict tail
    : param model : model
    """

    from pykeen.predict import get_tail_prediction_df

    df = get_tail_prediction_df(
        model=model,
        head_label=head,
        relation_label=relation,
        triples_factory=triples_factory,
    )

    return df.head(top_k)[["tail_label", "score"]]
