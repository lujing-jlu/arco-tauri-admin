from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You may want to restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

have_read_ids: List[int] = []


def success_response_wrap(data):
    return {
        "data": data,
        "status": "ok",
        "msg": "请求成功",
        "code": 20000,
    }

def get_message_list():
    return [
        {
            "id": 1,
            "type": "message",
            "title": "郑曦月",
            "subTitle": "的私信",
            "avatar": "//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/8361eeb82904210b4f55fab888fe8416.png~tplv-uwbnlip3yd-webp.webp",
            "content": "审批请求已发送，请查收",
            "time": "今天 12:30:01",
        },
        {
            "id": 2,
            "type": "message",
            "title": "宁波",
            "subTitle": "的回复",
            "avatar": "//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp",
            "content": "此处 bug 已经修复",
            "time": "今天 12:30:01",
        },
        {
            "id": 3,
            "type": "message",
            "title": "宁波",
            "subTitle": "的回复",
            "avatar": "//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp",
            "content": "此处 bug 已经修复",
            "time": "今天 12:20:01",
        },
        {
            "id": 4,
            "type": "notice",
            "title": "续费通知",
            "subTitle": "",
            "avatar": "",
            "content": "您的产品使用期限即将截止，如需继续使用产品请前往购…",
            "time": "今天 12:20:01",
            "messageType": 3,
        },
        {
            "id": 5,
            "type": "notice",
            "title": "规则开通成功",
            "subTitle": "",
            "avatar": "",
            "content": "内容屏蔽规则于 2021-12-01 开通成功并生效",
            "time": "今天 12:20:01",
            "messageType": 1,
        },
        {
            "id": 6,
            "type": "todo",
            "title": "质检队列变更",
            "subTitle": "",
            "avatar": "",
            "content": "内容质检队列于 2021-12-01 19:50:23 进行变更，请重新…",
            "time": "今天 12:20:01",
            "messageType": 0,
        },
    ]


@app.get("/api/message/list", response_model=List[Dict])
async def get_message_list_api():
    return get_message_list()


@app.post("/api/message/read", response_model=bool)
async def mark_messages_as_read(request: Request):
    body = await request.json()
    ids = body.get("ids", [])
    have_read_ids.extend(ids)
    return True

user_role = "admin"  # 初始用户角色，默认为 admin


def is_login():
    return user_role is not None


def get_user_info():
    if is_login():
        return {
            "name": "王立群",
            "avatar": "//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png",
            "email": "wangliqun@email.com",
            "job": "frontend",
            "jobName": "前端艺术家",
            "organization": "Frontend",
            "organizationName": "前端",
            "location": "beijing",
            "locationName": "北京",
            "introduction": "人潇洒，性温存",
            "personalWebsite": "https://www.arco.design",
            "phone": "150****0000",
            "registrationDate": "2013-05-10 12:10:00",
            "accountId": "15012312300",
            "certification": 1,
            "role": user_role,
        }
    else:
        return None


@app.post("/api/user/info", response_model=Dict)
async def get_user_info_api():
    info = get_user_info()
    return success_response_wrap(info)


@app.post("/api/user/login", response_model=Dict)
async def user_login(request: Request):
    body = await request.json()
    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="用户名和密码不能为空")

    global user_role
    if username == "admin" and password == "admin":
        user_role = "admin"
        token_data = {"token": "12345"}
        return success_response_wrap(token_data)
    elif username == "user" and password == "user":
        user_role = "user"
        token_data = {"token": "54321"}
        return success_response_wrap(token_data)
    else:
        raise HTTPException(status_code=401, detail="账号或密码错误")


@app.post("/api/user/logout", response_model=Dict)
async def user_logout():
    global user_role
    user_role = None
    return {"message": "登出成功"}


@app.get("/api/user/menu", response_model=List[Dict])
async def get_user_menu():
    menu_list = [
        {
            "path": "/dashboard",
            "name": "dashboard",
            "meta": {
                "locale": "menu.server.dashboard",
                "requiresAuth": True,
                "icon": "icon-dashboard",
                "order": 1,
            },
            "children": [
                {
                    "path": "workplace",
                    "name": "Workplace",
                    "meta": {"locale": "menu.server.workplace", "requiresAuth": True},
                },
                {
                    "path": "https://arco.design",
                    "name": "arcoWebsite",
                    "meta": {"locale": "menu.arcoWebsite", "requiresAuth": True},
                },
            ],
        }
    ]
    return success_response_wrap(menu_list)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)

