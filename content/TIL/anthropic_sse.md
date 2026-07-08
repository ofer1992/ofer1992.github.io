Title: Anthropic API SSE and Eager Tool Dispatch
Date: 2026-07-08 17:44
Category: TIL
Status: published

Today I was looking at how Eager Tool Dispatch might be implemented. That's when you execute tool calls while they are streaming. It might sound finicky at first, perhaps you need to parse partial jsons. Luckily that's not the case.

Anthropic API responses are streamed using SSE (server-sent events). Let's start with an example. Imagine you send "what's the weather in SF and NYC?" to an agent with a `get_weather` function.

The streaming response might look something like this.

```
+   0ms  message_start        usage.input_tokens=620, output_tokens=5
+   0ms  ping
+   0ms  [idx 0] content_block_start   <text>
+   0ms  [idx 0] content_block_delta   text="I'll check the current"
+ 433ms  [idx 0] content_block_delta   text=" weather in both cities" ...
+ 435ms  [idx 0] content_block_stop
+ 435ms  [idx 1] content_block_start   <tool_use id=toolu_vrtx_01ANbu… name=get_weather>
+ 435ms  [idx 1] content_block_delta   partial_json=''
+ 777ms  [idx 1] content_block_delta   partial_json='{"city":'
+ 778ms  [idx 1] content_block_delta   partial_json=' "San Francis'
+ 778ms  [idx 1] content_block_delta   partial_json='co"'
+ 786ms  [idx 1] content_block_delta   partial_json=', "unit": "celsius"}'
+ 789ms  [idx 1] content_block_stop        ◄── ETD fires: dispatch get_weather(SF) now
+ 789ms  [idx 2] content_block_start   <tool_use id=toolu_vrtx_02XyZq… name=get_weather>
+ 790ms  [idx 2] content_block_delta   partial_json=''
+1002ms  [idx 2] content_block_delta   partial_json='{"city":'
+1003ms  [idx 2] content_block_delta   partial_json=' "New Yor'
+1004ms  [idx 2] content_block_delta   partial_json='k"'
+1010ms  [idx 2] content_block_delta   partial_json=', "unit": "celsius"}'
+1011ms  [idx 2] content_block_stop        ◄── ETD fires: dispatch get_weather(NYC) now
+1013ms  message_delta        stop_reason=tool_use, output_tokens=142
+1013ms  message_stop

```

Each event has a type (`message_start/delta/stop`, `content_block_start/delta/stop`) and content. The response is a sequence of content blocks, each is either text or a tool call, the content is a partial "delta" which you can concatenate, and it explicitly tells you when a block ends, at which point you know you have the full tool call. This let's you dispatch the `get_weather` call to SF while you wait for the tool call to NY, saving some latency.
