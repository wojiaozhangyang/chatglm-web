import os
import uvicorn
import json
import traceback
import uuid
import requests

from apig_sdk import signer
from os.path import abspath, dirname
from loguru import logger
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from message_store import MessageStore
# from transformers import AutoModel, AutoTokenizer
from errors import Errors
# import knowledge
# import gen_data
import pandas as pd

log_folder = os.path.join(abspath(dirname(__file__)), "log")
logger.add(os.path.join(log_folder, "{time}.log"), level="INFO")


DEFAULT_DB_SIZE = 100000

massage_store = MessageStore(db_path="message_store.json", table_name="chatgpt", max_size=DEFAULT_DB_SIZE)
# Timeout for FastAPI
# service_timeout = None

app = FastAPI()
# app = Flask(__name__)

stream_response_headers = {
    "Content-Type": "application/octet-stream",
    "Cache-Control": "no-cache",
}


@app.post("/config")
async def config():
    return JSONResponse(content=dict(
        message=None,
        status="Success",
        data=dict()
    ))



async def process(prompt, result,options, params, message_store, is_knowledge, history=None):
    """
    发文字消息
    """
    # 不能是空消息
    if not prompt:
        logger.error("Prompt is empty.")
        yield Errors.PROMPT_IS_EMPTY.value
        return


    try:
        chat = {"role": "user", "content": prompt}

        # 组合历史消息
        if options:
            parent_message_id = options.get("parentMessageId")
            messages = message_store.get_from_key(parent_message_id)
            if messages:
                messages.append(chat)
            else:
                messages = []
        else:
            parent_message_id = None
            messages = [chat]

        # 记忆
        messages = messages[-params['memory_count']:]


        history_formatted = []
        if options is not None:
            history_formatted = []
            tmp = []
            for i, old_chat in enumerate(messages):
                if len(tmp) == 0 and old_chat['role'] == "user":
                    tmp.append(old_chat['content'])
                elif old_chat['role'] == "AI":
                    tmp.append(old_chat['content'])
                    history_formatted.append(tuple(tmp))
                    tmp = []
                else:
                    continue

        uid = "chatglm"+uuid.uuid4().hex
        footer=''
        # if is_knowledge:
        #     response_d = knowledge.find_whoosh(prompt)
        #     output_sources = [i['title'] for i in response_d]
        #     results ='\n---\n'.join([i['content'] for i in response_d])
        #     prompt=  f'system:基于以下内容，用中文简洁和专业回答用户的问题。\n\n'+results+'\nuser:'+prompt
        #     footer=  "\n参考：\n"+('\n').join(output_sources)+''
        # yield footer
				# lines = result.splitlines()


        for response in result.splitlines():
            message = json.dumps(dict(
                role="AI",
                id=uid,
                parentMessageId=parent_message_id,
                text=result,
            ))
            yield "data: " + message

    except:
        err = traceback.format_exc()
        logger.error(err)
        yield Errors.SOMETHING_WRONG.value
        return

    try:
        # save to cache
        chat = {"role": "AI", "content": response}
        messages.append(chat)

        parent_message_id = uid
        message_store.set(parent_message_id, messages)
    except:
        err = traceback.format_exc()
        logger.error(err)


# @app.post("/chat-process")
# async def chat_process(request_data: dict):
#     prompt = request_data['prompt']
#     max_length = request_data['max_length']
#     top_p = request_data['top_p']
#     temperature = request_data['temperature']
#     options = request_data['options']
#     if request_data['memory'] == 1 :
#         memory_count = 5
#     elif request_data['memory'] == 50:
#         memory_count = 20
#     else:
#         memory_count = 999
#
#     if 1 == request_data["top_p"]:
#         top_p = 0.2
#     elif 50 == request_data["top_p"]:
#         top_p = 0.5
#     else:
#         top_p = 0.9
#     if temperature is None:
#         temperature = 0.9
#     if top_p is None:
#         top_p = 0.7
#     is_knowledge = request_data['is_knowledge']
#     params = {
#         "max_length": max_length,
#         "top_p": top_p,
#         "temperature": temperature,
#         "memory_count": memory_count
#     }
#     answer_text = process(prompt, options, params, massage_store, is_knowledge)
#     return StreamingResponse(content=answer_text, headers=stream_response_headers, media_type="text/event-stream")

async def generate_result(prompt,result):
	chat = {"role": "user", "content": prompt}
	uid = "chatglm" + uuid.uuid4().hex
	parent_message_id = None
	messages = [chat]
	message = json.dumps(dict(
		role="AI",
		id=uid,
		parentMessageId=parent_message_id,
		text= result,
	))
	yield "data: " + result

	# lines = result.splitlines()
	# for line in lines:
	# 	yield line.encode('utf-8')

@app.post("/chat-process")
async def chat_process(request_data: dict):
	print("======================")
	# 读取表格文件

	df = pd.read_excel('vv.xlsx',   header=None)
	prompt = request_data['prompt']
	max_length = request_data['max_length']
	top_p = request_data['top_p']
	temperature = request_data['temperature']
	options = request_data['options']
	if request_data['memory'] == 1 :
			memory_count = 5
	elif request_data['memory'] == 50:
			memory_count = 20
	else:
			memory_count = 999

	if 1 == request_data["top_p"]:
			top_p = 0.2
	elif 50 == request_data["top_p"]:
			top_p = 0.5
	else:
			top_p = 0.9
	if temperature is None:
			temperature = 0.9
	if top_p is None:
			top_p = 0.7
	is_knowledge = request_data['is_knowledge']
	params = {
			"max_length": max_length,
			"top_p": top_p,
			"temperature": temperature,
			"memory_count": memory_count
	}
	# 根据第二列进行匹配
	keyword = prompt
	filtered_df = df[df[1] == keyword]
	if filtered_df.empty:
			url = "https://e34e30bda81f4586a03250b37a863d36.infer.xckpjs.com/v1/infers/d8250d26-6a42-40ba-9454-0ff93119576b"
			method = 'POST'

			# Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
			headers = {"content-type": "application/json"}
			# Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
			body = {
				"prompt": prompt,
				"history": [],
				"max_length": max_length | 2048,
				"top_p": top_p,
				"temperature": temperature
			}

			r = signer.HttpRequest(method, url, headers, json.dumps(body))
			sig = signer.Signer()
			# Set the AK/SK to sign and authenticate the request.
			sig.Key = "LWYFNIIRUKPRQUYSBZPY"
			sig.Secret = "NNv1sCj6ufH4h82Q9fQCoLl6JDeUfEYdvFkOHqo0"
			sig.Sign(r)
			# print(r.headers["content-type"])
			# print(r.headers["Authorization"])

			resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body, verify=False)
			decoded_content = resp.content.decode('utf-8')

			response_value = ''
			try:
				response_data = json.loads(decoded_content)
				if 'response' in response_data:
					response_value = response_data['response']
					# print(response_value)
				else:
					response_value = "No 'response' field found in JSON."
			except json.JSONDecodeError as e:
				response_value  ="Error decoding JSON:", str(e)
			except Exception as e:
				response_value = "An error occurred:", str(e)


			answer_text = process(prompt, response_value, options, params, massage_store, is_knowledge)
			return StreamingResponse(content=answer_text, headers=stream_response_headers, media_type="text/event-stream")
			# print(decoded_content)
			# print(response_value)
	else:
			# 获取匹配结果的第三列内容
			result = filtered_df.iloc[0, 2]
			answer_text = process(prompt, result, options, params, massage_store, is_knowledge)
			# answer_text = generate_result(prompt, result)

			return StreamingResponse(content=answer_text, headers=stream_response_headers, media_type="text/event-stream")
	#return StreamingResponse(content=result, headers=stream_response_headers, media_type="text/event-stream")


if __name__ == "__main__":
		uvicorn.run(app, host='0.0.0.0', port=3002)
		# app.run(host='0.0.0.0', port=3002)
