import weaviate
from weaviate.auth import AuthApiKey
import weaviate.classes as wvc
from weaviate.classes.config import Property, DataType
import ollama



# 本地部署的
# client = weaviate.connect_to_local(
#     auth_credentials=AuthApiKey("test-secret-key")
# )
# 示例数据
documents = [
  "教育部出台这份文件是为了进一步完善体育教师队伍建设体制机制，努力打造一支高素质专业化的中小学体育教师队伍，为加快建设教育强国、体育强国贡献力量",
  "作为首个专门针对体育教师队伍建设的文件，《通知》结合实际问题，总结分析体育教师队伍的特点、现状、问题，聚焦补充配备、专业提升、待遇保障，提出了一些创新做法",
  "第一，突出体育教师补充配备。一是在充分调研和科学测算基础上，提出学校要按照不高于班师比小学5：1、初中6：1、高中8：1的标准配备体育专任教师，并且针对体育教师招聘条件做了明确要求",
  "第二，突出体育教师专业素质提升。一是提高来源质量，规定体育教师的学历须是体育专业，非体育专业要具有二级及以上运动员等级证书",
  "第三，突出体育教师队伍待遇保障",
  "第四，突出对“三大球”教师队伍的重视",
]

client = weaviate.connect_to_custom(
    skip_init_checks=False,
    http_host="172.30.72.177",
    http_port=8080,
    http_secure=False,
    grpc_host="172.30.72.177",
    grpc_port=50051,
    grpc_secure=False,
    # 对应AUTHENTICATION_APIKEY_ALLOWED_KEYS中的密钥
    # 注意：此处只需要密钥即可，不需要用户名称
    auth_credentials=AuthApiKey("test-secret-key")
)




# 嵌入式向量
collection = client.collections.get(
    name = "docs", # Name of the data collection
    # properties=[
    #     Property(name="text", data_type=DataType.TEXT), # Name and data type of the property
    # ],
)

with collection.batch.dynamic() as batch:
    for i,d in enumerate(documents):
        response = ollama.embeddings(model='all-minilm:33m', prompt=d)
        print(response)
        batch.add_object(
            properties={"text":d},
            vector= response["embedding"]
        )

prompt = "教育部分出台《通知》的目的?"

# Generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(
  model = "all-minilm:33m",
  prompt = prompt,
)

results = collection.query.near_vector(near_vector = response["embedding"],
                                       limit = 1)
print(results)

data = results.objects[0].properties['text']

print(data)
prompt_template = f"使用这个数据: {data}. 回答这个问题: {prompt}"
print(prompt_template)
output = ollama.generate(
  model = "deepseek-r1:8b",
  prompt = prompt_template,
)

print(output['response'])