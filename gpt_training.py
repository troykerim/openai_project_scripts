from openai import OpenAI

client = OpenAI(api_key="")  
suffix_name = "model_name"

client.fine_tuning.jobs.create(
  training_file="file-xxxxxxxxxxxxxxxxxxxxxxx",
  model="gpt-4o-2024-08-06",
  suffix=suffix_name,
  hyperparameters={
    "n_epochs": 1,     
    "learning_rate_multiplier": 1,  
    "batch_size": 1,
  }
)