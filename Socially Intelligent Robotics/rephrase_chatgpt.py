from sic_framework.services.openai_gpt.gpt import GPT, GPTResponse, GPTConf, GPTRequest

# Read OpenAI key from file
with open("openai_key", "rb") as f:
    openai_key = f.read().decode("utf-8").strip()  # Decode bytes to string and remove new line character

# Setup GPT
conf = GPTConf(openai_key=openai_key)
gpt = GPT(conf=conf)

# Function to get rephrased sentence from GPT
def get_rephrased_sentence(sentence):
    # Prepare the prompt for rephrasing
    prompt = f"Rephrase the following sentence: {sentence}"

    # Get reply from model
    reply = gpt.request(GPTRequest(prompt))
    return reply.response

# Main interaction
if __name__ == '__main__':
    # Ask for user input
    original_sentence = input("Enter a sentence to rephrase:\n-->")

    # Get rephrased sentence from GPT
    rephrased_sentence = get_rephrased_sentence(original_sentence)
    print("\nRephrased Sentence:\n", rephrased_sentence)
