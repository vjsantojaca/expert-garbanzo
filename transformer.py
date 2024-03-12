import yaml


if __name__ == '__main__':

  with open('bot.yaml', 'r') as file:
    prime_service = yaml.safe_load(file)

  print (prime_service["inboundShortMessage"]["name"])