# Hướng dẫn kết nối FastAPI với PostgreSQL dùng SQLModel

Tài liệu này hướng dẫn bạn cấu hình kết nối cơ sở dữ liệu PostgreSQL cho ứng dụng FastAPI bằng ORM SQLModel, cách khởi tạo bảng, và cách sử dụng Session trong endpoint.

## 1) Thành phần chính trong repo

- app/core/settings.py: Đọc biến môi trường (.env) và dựng DATABASE_URL. Có hỗ trợ tự động build URL từ POSTGRES_*
- app/core/database.py: Khởi tạo SQLModel engine + dependency get_db
- app/shared/database.py: Re-export engine, get_db để import dùng chung
- app/tools/init_db.py: Script tạo bảng (create_all)
- app/main.py: Khởi tạo FastAPI, cấu hình logging + OpenAPI và gắn router tính năng
- app/features/auth/domain/account.py: Ví dụ model Account (SQLModel)
- app/features/auth/api/router.py: Router auth (register, login, me) dùng dependency get_db

## 2) Cấu hình môi trường (.env)

Bạn có thể dùng 1 trong 2 cách:

1. Đặt trực tiếp DATABASE_URL:

    DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DB_NAME

2. Hoặc đặt các biến POSTGRES_* (Settings sẽ tự dựng DATABASE_URL, mặc định POSTGRES_HOST=db khi chạy docker-compose):

    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=thesis_hub
    POSTGRES_HOST=localhost

Các biến bổ sung:

- DEBUG=true|false
- AUTO_CREATE_TABLES=true|false (mặc định true trong dev; app sẽ tự tạo bảng ở sự kiện startup)

## 3) Cài đặt và chạy (local)

1. Tạo môi trường ảo và cài requirements:
   - python -m venv .venv
   - .venv\\Scripts\\activate
   - pip install -r requirements.txt

2. Đảm bảo PostgreSQL đang chạy và .env đã được cấu hình.

3. Khởi chạy API:
   - uvicorn app.main:app --reload

4. Tạo bảng (nếu chưa có):
   - python -m app.tools.init_db

## 4) Chạy bằng docker-compose

Repo có sẵn docker-compose.yml với 2 services: db (Postgres) và api.

1. Chuẩn bị file .env ở thư mục gốc (tham khảo mục 2).
2. Chạy: docker compose up -d
3. Xem API: http://localhost:8000/docs

Ghi chú: Biến POSTGRES_HOST trong container api được set thành db để kết nối tới service Postgres nội bộ.

## 5) Cách hoạt động của kết nối

- app/core/database.py dùng SQLModel.create_engine(DATABASE_URL, pool_pre_ping=True)
- Dependency get_db() cung cấp Session cho mỗi request:

    from sqlmodel import Session
    from fastapi import Depends
    from app.core.database import get_db

    @router.get("/items")
    def list_items(db: Session = Depends(get_db)):
        return db.exec(select(Item)).all()

## 6) Khởi tạo bảng

Có 2 cách:

1. Thủ công (khuyến nghị): chạy python -m app.tools.init_db sau khi DB sẵn sàng.
2. Tuỳ chọn (dev): có biến cấu hình AUTO_CREATE_TABLES trong settings, nhưng hiện chưa bật tự động tạo bảng trong app/main.py. Bạn có thể tự thêm logic này vào sự kiện startup nếu muốn.

Lưu ý: Trong production, nên dùng Alembic để migrate thay vì create_all tự động.

### Quản lý schema bằng Alembic (đã cấu hình sẵn)

Repo đã tích hợp Alembic với cấu trúc:

- alembic.ini (cấu hình Alembic, script_location=migrations)
- migrations/
  - env.py (nạp DATABASE_URL từ app.core.settings, target_metadata = SQLModel.metadata)
  - script.py.mako (template)
  - versions/
    - 0001_create_users_table.py (migration khởi tạo bảng users của auth)

Cách dùng cơ bản:

1. Tạo migration mới (autogenerate) khi thay đổi models:

   alembic revision --autogenerate -m "your message"

2. Áp dụng migration lên DB:

   alembic upgrade head

3. Quay lui:

   alembic downgrade -1

Ghi chú:

- Không cấu hình sqlalchemy.url trong alembic.ini; env.py sẽ lấy từ settings.DATABASE_URL (đọc từ .env hoặc POSTGRES_*).
- Đảm bảo các models được import trong migrations/env.py để autogenerate thấy đủ metadata (đã import app.features.auth.domain.account mặc định).

## 7) Ví dụ model và CRUD

- Model mẫu: app/features/auth/domain/account.py
- CRUD mẫu: app/features/auth/application/crud.py (dùng Session để query/commit)

## 8) Swagger và bảo mật

- Swagger UI: /docs, ReDoc: /redoc
- Hệ thống auth mẫu sử dụng JWT, có flow login/register; xem app/features/auth

## 9) Sự cố thường gặp

- DATABASE_URL trống: đảm bảo đặt DATABASE_URL hoặc đủ POSTGRES_USER/POSTGRES_PASSWORD/POSTGRES_DB
- Kết nối từ Windows: nếu chạy Postgres trong docker, POSTGRES_HOST=localhost khi chạy local; còn trong container api, POSTGRES_HOST=db
- Chưa có bảng: hãy chạy python -m app.tools.init_db để tạo bảng (hoặc dùng Alembic: alembic upgrade head)

## 10) Luồng chạy theo thư mục (từ startup đến xử lý request)

Phần này mô tả cách các thư mục/module phối hợp trong quá trình khởi động ứng dụng và xử lý một request điển hình.

- app/main.py
  - Gọi setup_logging(...) từ app/core/logging_config.py để cấu hình log console.
  - Khởi tạo FastAPI(app) kèm tiêu đề, phiên bản, đường dẫn OpenAPI/Swagger.
  - Gắn router của từng tính năng, ví dụ: app/features/auth/api/router.py được mount tại prefix /auth.
  - Tuỳ biến OpenAPI để thêm bearerAuth (JWT) thông qua app/core/openapi.py.

- app/core/
  - settings.py: nạp biến môi trường (.env), dựng DATABASE_URL (hoặc từ POSTGRES_*), cờ DEBUG, v.v.
  - database.py: tạo SQLModel engine và khai báo dependency get_db() trả về Session cho mỗi request.
  - logging_config.py: cấu hình logging dạng dictConfig.
  - openapi.py: chèn securitySchemes Bearer JWT và áp dụng global security cho OpenAPI.

- app/shared/
  - database.py: re-export engine, get_db để các module dùng thống nhất (import từ app.shared.database).

- app/features/auth/
  - api/
    - router.py: định nghĩa endpoints /register, /login, /me; dùng Depends(get_db) và các deps bảo mật.
    - dependencies.py: định nghĩa get_current_user, get_current_active_user; decode JWT, tìm user trong DB.
  - application/
    - crud.py: nghiệp vụ truy cập dữ liệu (get_user_by_email, create_user, authenticate_user).
  - domain/
    - account.py: định nghĩa model bảng (Account) với SQLModel.
    - schemas.py: các schema Pydantic cho request/response (UserCreate, UserRead, Token...).
  - infrastructure/
    - security/tokens.py: băm mật khẩu, tạo/giải mã JWT, cấu hình thuật toán/secret.

- app/tools/
  - init_db.py: script tạo bảng dựa trên SQLModel.metadata và engine.

- migrations/
  - env.py: cấu hình Alembic, nạp DATABASE_URL từ settings và import models để target_metadata đầy đủ.
  - versions/: chứa các migration đã tạo.

Luồng khởi động (ví dụ chạy uvicorn app.main:app --reload):
1) Python import app.main → hàm create_app() chạy: cấu hình logging, tạo FastAPI, include router, tuỳ biến OpenAPI.
2) Khi có request đến (ví dụ POST /auth/login), FastAPI định tuyến tới handler tương ứng trong app/features/auth/api/router.py.

Luồng xử lý 1 request điển hình (POST /auth/login):
1) Router nhận form OAuth2 (username/password) qua OAuth2PasswordRequestForm.
2) Depends(get_db) mở một Session (app/core/database.py) và cung cấp cho handler.
3) Handler gọi application.crud.authenticate_user →
   - crud.get_user_by_email truy cập DB qua Session
   - verify_password so sánh mật khẩu (infrastructure/security/tokens.py)
4) Nếu hợp lệ, tạo JWT bằng tokens.create_access_token và trả về schema Token.

Luồng bảo vệ endpoint (GET /auth/me):
1) dependencies.get_current_active_user phụ thuộc get_current_user → rút token từ header Authorization: Bearer.
2) tokens.decode_token giải mã JWT để lấy email (sub), sau đó crud.get_user_by_email tải user từ DB.
3) Trả về thông tin user theo schema UserRead.

Gợi ý: Khi thêm tính năng mới, tạo thư mục dưới app/features/<feature>/ với cấu trúc tương tự (api/application/domain/infrastructure). Router mới được include trong app/main.py.
