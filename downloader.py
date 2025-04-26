import requests
import time
import json

# Function to get block data from Blockchair
def get_blockchair_block(block_index):
    url = f"https://blockchain.info/rawblock/{block_index}"
    response = requests.get(url)
    # print(json.dumps(response.json(), indent=4))
    # print("\n\n")
    return response.json()

# Function to check transaction outputs and write to a file
def check_outputs_and_write_to_file(block_data):
    with open("allpubs.txt", "a") as file:
        for tx in block_data['tx']:
            for output in tx['out']:
                if output['value'] > 0 and not output['spent']:
                    pub = output['script']
                    file.write(f"{pub[2:132]}\n")
            return
                # else:
                #     pub = output['script']
                #     file.write(f"{pub[2:132]} ZERO\n")

# Main loop to iterate over block indices
blockchair_data_index = 1

while True:
    try:
        with open('checked.json', 'w') as f:
            json.dump({'block_index': blockchair_data_index}, f)
        # Retrieve block data from Blockchair
        blockchair_data = get_blockchair_block(blockchair_data_index)
        
        # Check outputs and write pkscripts to the file if conditions are met
        check_outputs_and_write_to_file(blockchair_data)
        
        # Increment block index for the next iteration
        blockchair_data_index += 1
        
        # Add delay to prevent overloading the API (adjust as necessary)
        time.sleep(2)

    except Exception as e:
        print(f"Error fetching or processing block: {e}")
        time.sleep(5)  # Delay before retrying in case of error
