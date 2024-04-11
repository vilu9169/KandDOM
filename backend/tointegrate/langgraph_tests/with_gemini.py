from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph
from langchain_google_vertexai import VertexAI
from langchain_anthropic import AnthropicLLM


model = VertexAI(model_name="gemini-pro")

graph = MessageGraph()

graph.add_node("oracle", model)
graph.add_node("node2", model)
graph.add_node("node3", model)
graph.add_node("node4", model)
graph.add_node("node5", model)
graph.add_node("node6", model)

graph.add_edge("oracle", "node2")
graph.add_edge("node2", "node3")
graph.add_edge("node3", "node4")
graph.add_edge("node4", "node5")
graph.add_edge("node5", "node6")
graph.add_edge("node6", END)


graph.set_entry_point("oracle")

runnable = graph.compile()

print("graph compiled")

message = "give me a recipe for a cake"

#output = model.invoke(message)
# output = runnable.invoke(HumanMessage("What is 1 + 1?"))

inputs  = HumanMessage("Let's rhyme on the word cat, repeasts are not allowed. I'll start: 'hat'")
# print(output)

for output in runnable.stream(inputs):
    # stream() yields dictionaries with output keyed by node name
    for key, value in output.items():
        print(f"Output from node '{key}':")
        print("---")
        print(value)
    print("\n---\n")

