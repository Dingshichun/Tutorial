"""
# RESTful API 的使用，定义一个最简单的 API
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask RESTful API!"

if __name__ == '__main__':
    app.run(debug=True)
"""

# 一个完整的 RESTful API，包含了获取所有用户、获取单个用户、创建新用户、更新用户和删除用户等操作
# 默认情况下，Flask 应用会在 http://127.0.0.1:5000/ 启动。
# 测试 API：您可以使用工具如 Postman 或 curl来测试 API。以下是一些示例 bash 命令：
# 1、获取所有用户的 bash 命令：curl http://127.0.0.1:5000/users
# 2、获取单个用户的 bash 命令：curl http://127.0.0.1:5000/users/1
# 3、创建新用户的 bash 命令：curl -X POST -H "Content-Type: application/json" -d '{"name":"Alice","email":"alice@example.com"}' http://127.0.0.1:5000/users
# 4、更新用户的 bash 命令：curl -X PUT -H "Content-Type: application/json" -d '{"name":"Alice Smith","email":"alice.smith@example.com"}' http://127.0.0.1:5000/users/3
# 5、删除用户的 bahs 命令：curl -X DELETE http://127.0.0.1:5000/users/3

# 开发完成后可以部署到生产环境，可以使用 Gunicorn 或 uWSGI 来部署 Flask 应用。
# 也可以使用Nginx 和 Gunicorn：在生产环境中，通常会使用 Nginx 作为反向代理服务器，将请求转发给 Gunicorn。
from flask import Flask, jsonify, request

app = Flask(__name__)  # 创建一个 Flask 应用

# 模拟数据
users = [
    {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
]


# 获取所有用户
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


# 获取单个用户
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


# 创建新用户
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
    users.append(new_user)
    return jsonify(new_user), 201


# 更新用户
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    user["name"] = data["name"]
    user["email"] = data["email"]
    return jsonify(user)


# 删除用户
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    user = next((user for user in users if user["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "User deleted"}), 204


if __name__ == "__main__":
    app.run(debug=True)  # 启动 Flask 应用
