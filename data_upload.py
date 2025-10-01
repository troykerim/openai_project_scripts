from openai import OpenAI

client = OpenAI(api_key="")


training_file = client.files.create(
  file=open(r"", "rb"),
  purpose="fine-tune"
)
# validation_file = client.files.create(
#   file=open("validation_set.jsonl", "rb"),
#   purpose="fine-tune"
# )


print('train_id', training_file.id)
# print('val_id', validation_file.id)