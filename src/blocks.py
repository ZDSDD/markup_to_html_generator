from enum import Enum, auto

from .htmlnode import HTMLNode, ParentNode, LeafNode


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def markdown_to_block(markdown: str) -> list[str]:
    return markdown.split("\n\n")


def block_to_block_type(text_block: str) -> BlockType:
    if isHeading(text_block):
        return BlockType.HEADING
    elif isCode(text_block):
        return BlockType.CODE
    elif isQuote(text_block):
        return BlockType.QUOTE
    elif isOrderedList(text_block):
        return BlockType.ORDERED_LIST
    elif isUnOrderedList(text_block):
        return BlockType.UNORDERED_LIST

    return BlockType.PARAGRAPH


def isOrderedList(text_block: str):
    lines = text_block.split("\n")
    for index, line in enumerate(lines, start=1):
        if len(line) < 3:
            return False
        if line[0] != str(index):
            return False
        if line[2] != " ":
            return False

    return True


def isUnOrderedList(text_block: str):
    lines = text_block.split("\n")
    for line in lines:
        if len(line) < 1:
            return False
        if line[0] != "*" and line[0] != "-":
            return False
    return True


def isQuote(string: str):
    return string[0] == ">"


def isCode(string: str):
    string = string.strip()
    if len(string) < 6:
        return False
    return string[:3] == "```" and string[-3:] == "```"


def isHeading(string: str) -> bool:

    if len(string) < 2:
        return False
    if string[0] != "#":
        return False

    counter = 0

    for character in string:
        if character == "#":
            counter += 1
        else:
            break
        if counter > 6:
            return False
    return True


def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    blocks = [block.strip('\n') for block in blocks]
    child_nodes: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            heading_node = LeafNode(f'h{get_heading_level(block)}', format_heading_to_html(block))
            child_nodes.append(heading_node)
        if block_type == BlockType.CODE:
            code_node = LeafNode("code", format_code_for_html(block))
            code_wrapper_node = ParentNode("pre", [code_node])
            child_nodes.append(code_wrapper_node)
        if block_type == BlockType.QUOTE:
            quote_node = LeafNode("blockquote", format_quote_to_html(block))
            child_nodes.append(quote_node)
        if block_type == BlockType.UNORDERED_LIST:
            ul_items = [LeafNode("li",item) for item in format_list_to_html(block)]
            parent_ulist = ParentNode('ul', ul_items)
            child_nodes.append(parent_ulist)
        if block_type == BlockType.ORDERED_LIST:
            ul_items = [LeafNode("li",item) for item in format_list_to_html(block)]
            parent_ulist = ParentNode('ol', ul_items)
            child_nodes.append(parent_ulist)
        if block_type == BlockType.PARAGRAPH:
            child_nodes.append(LeafNode('p', block))
            
        for node in child_nodes:
            print(node.to_html())

def get_heading_level(block: str) -> int:
    counter:int = 0
    for character in block:
        if character == '#':
            counter += 1
        else:
            break
    return counter

def format_heading_to_html(block: str) -> str:
    return block[get_heading_level(block):]

def format_list_to_html(block: str) -> list[str]:
    return [str[2:] for str in block.split('\n')]

def format_code_for_html(code_block):
    return code_block[3:-3]


def format_quote_to_html(code_block):
    return code_block[1:]


if __name__ == "__main__":
    markdown_to_html_node(
        """## Installation

### Download the project

Download `.zip` file or run commads from your favourite CLI

```bash
git clone https://github.com/ZDSDD/IoT_OpcAgent.git
cd IoT_OpcAgent
```

### How to run IoT Agent

To run the application, you can [build it yourself](https://stackoverflow.com/questions/44074121/build-net-core-console-application-to-output-an-exe), or run the OpcAgent.exe

### How to run Azure Function

As the above, or [deploy](#deploy-to-azure) it to Azure so it can run constantly and listen for the requests.

## Configuration

This section will show which local variables need to be set up, both on Azure App and on the OPC Agent.

### Local Configuration for Function Apps

This sample local.settings.json file should be located in the root folder of the FunctionAppsDemo solution.

```json
{
    "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "AzureWebJobsStorageConnectionStringValue",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet",
    "ServiceBusConnectionString": "<my_service_bus_connection_string>",
    "QueueNameProduction": "<name_of_my_created_queue1>",
    "QueueNameErrorEvent": "<name_of_my_created_queue2>",
    "QueueNameThreeErrors": "<name_of_my_created_queue3>",
    "ThreeErrorsBlobContainerName": "<blob_container_name_in_azure>",
    "productionBlobContainerName": "<blob_container_name_in_azure>",
    "IoTHubConnectionString": "<my_IoTHuB_connection_string>",
    "Storage": "<my_storage_connection_string>",
    "CommunicationServiceConnectionString": "<my_communication_service_connection_string>",
    "senderAddress": "<email_that_sends_emails>",
    "emailTo": "<some@mail.com>"
  }
}
```

* This is the first list item in a list block
* This is a list item
* This is another list item

1. lsit1
2. l;ist2
3. ogórek


### Deploy to Azure 

If deployed on Azure, navigate to Settings -> Environment variables -> **Add application setting**.

>Official Microsoft documentation app-service-settings [link](https://learn.microsoft.com/en-us/azure/app-service/reference-app-settings)
"""
    )
