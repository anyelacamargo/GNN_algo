import pandas as pd

def extract_metrics_pr(result, name):
    """
    Extract metrics early
    :param result: results from model type
    :param name: model name
    """

    m = result.metric_results.to_dict()

    return {
        "model": name,
        "MRR": m["both"]["mean_reciprocal_rank"],
        "Hits@10": m["both"]["hits_at_10"],
        "MRR_head": m["head"]["mean_reciprocal_rank"],
        "Hits@10_head": m["head"]["hits_at_10"],
        "MRR_tail": m["tail"]["mean_reciprocal_rank"],
        "Hits@10_tail": m["tail"]["hits_at_10"],
    }


def extract_metrics(result, name):
    """
    Extract metrics
    :param result: results from model type
    :param name: model name
    """

    mr = result.metric_results

    return {
        "model": name,

        # Overall
        "MRR": mr.get_metric("both.realistic.inverse_harmonic_mean_rank"),
        "Hits@10": mr.get_metric("both.realistic.hits_at_10"),

        # Head prediction
        "MRR_head": mr.get_metric("head.realistic.inverse_harmonic_mean_rank"),
        "Hits@10_head": mr.get_metric("head.realistic.hits_at_10"),

        # Tail prediction
        "MRR_tail": mr.get_metric("tail.realistic.inverse_harmonic_mean_rank"),
        "Hits@10_tail": mr.get_metric("tail.realistic.hits_at_10"),
    }


def compare_models(results_dict):
    """
    Compare models
    :param result_dict: load and pull model results
    """
    rows = []

    for name, result in results_dict.items():
        rows.append(extract_metrics(result, name))

    return pd.DataFrame(rows)
