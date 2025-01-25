import weaviate
from weaviate.auth import AuthApiKey

# 本地部署的
# client = weaviate.connect_to_local(
#     auth_credentials=AuthApiKey("test-secret-key")
# )

client = weaviate.connect_to_custom(
    skip_init_checks=False,
    http_host="172.20.8.178",
    http_port=8080,
    http_secure=False,
    grpc_host="172.20.8.178",
    grpc_port=50051,
    grpc_secure=False,
    # 对应AUTHENTICATION_APIKEY_ALLOWED_KEYS中的密钥
    # 注意：此处只需要密钥即可，不需要用户名称
    auth_credentials=AuthApiKey("test-secret-key")
)
print(client.is_ready())
print(client.close())