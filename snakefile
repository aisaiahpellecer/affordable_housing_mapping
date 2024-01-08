rule Web Scrape: 
  output:
    "data/urbanize.csv"
  shell:
    "python scripts/web_scrape.py"

rule Prepare: 
  input:
    "data/labeled.csv",
    "data/urbanize.csv"
  output:
    "figures/confusion_matrix_heatmap.png",
    "models/trained_MultinomialNB_classifier_model.joblib",
    "data/prediction.csv"
  shell:
    "python scripts/prepare_data.py"

rule Analyze:
  input:
    "data/prediction.csv",
    "data/boundaries.geojson"
  output:
    "data/predictions_mapping.geojson"
  shell:
    "python scripts/prediction_mapping.py"


rule Reproduce:
  input:
    "data/prediction.csv",
    "data/predictions_mapping.geojson",
    "figures/confusion_matrix_heatmap.png",
    "models/trained_MultinomialNB_classifier_model.joblib"