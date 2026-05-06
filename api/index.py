from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        return jsonify({"msg": "API running ✅"})

    try:
        data = request.get_json(force=True)

        eat = data.get("eat")
        uid = data.get("uid")
        password = data.get("pass")
        bio = data.get("bio")

        jwt = None

        # 🔹 EAT → ACCESS → JWT
        if eat:
            r1 = requests.get(f"https://9x-eat-to-access-coral.vercel.app/rizer?eat_token={eat}")
            d1 = r1.json()

            r2 = requests.get(f"https://9x-access-to-jwt.vercel.app/rizer?access_token={d1.get('access_token')}")
            d2 = r2.json()

            jwt = d2.get("jwt")

        # 🔹 UID + PASS login
        if uid and password:
            login = requests.post(
                "https://example.com/login",
                json={"uid": uid, "pass": password}
            )
            d = login.json()
            jwt = d.get("jwt")

        if not jwt:
            return jsonify({"error": "JWT not found"}), 400

        # 🔹 BIO UPLOAD
        r3 = requests.post(
            "https://9x-long.vercel.app/bio_upload",
            json={"jwt": jwt, "bio": bio}
        )

        return jsonify(r3.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔥 Vercel handler (IMPORTANT)
def handler(request, context):
    return app(request.environ, lambda *args: None)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)