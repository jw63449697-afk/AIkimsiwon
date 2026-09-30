# AI김시원 Discord Bot

사람이 직접 가르친 말을 SQLite에 저장하고, 저장된 답변 중 하나를 랜덤으로 말하는 수동형 Discord AI 봇입니다.

## 기능

- `/가르치기 말 답변`
- `/가르친횟수`
- `김시원 [말]` 형태의 일반 메시지 반응
- 같은 말에 여러 답변 저장
- 여러 답변 중 랜덤 선택
- 같은 서버의 모든 사용자가 학습 데이터 공유
- 서버별 학습 데이터 분리
- 중복 학습 방지
- SQLite 영구 저장
- Railway 배포 가능

## 예시

```text
/가르치기 사과 맛있어요!
```

이후:

```text
김시원 사과
```

→

```text
맛있어요!
```

다시:

```text
/가르치기 사과 상큼해요!
```

이후 `김시원 사과`를 입력하면:

```text
맛있어요!
```

또는

```text
상큼해요!
```

중 하나가 랜덤으로 나옵니다.

배우지 않은 말을 입력하면:

```text
# 가르치고 말이나 해
```

가 나옵니다.

## 로컬 실행

Python 3.11 이상을 권장합니다.

```bash
pip install -r requirements.txt
```

`.env.example`을 복사해서 `.env`를 만들고:

```env
BOT_TOKEN=디스코드_봇_토큰
DATABASE_PATH=data/kimsw.db
```

실행:

```bash
python main.py
```

## Discord Developer Portal 설정

봇의 Bot 설정에서 **Message Content Intent**를 활성화해야 합니다.

또한 봇을 서버에 초대할 때 애플리케이션 명령어(Slash Commands)를 사용할 수 있는 권한으로 초대해야 합니다.

## Railway

GitHub 저장소를 Railway에 연결한 뒤 Variables에:

```text
BOT_TOKEN=디스코드_봇_토큰
DATABASE_PATH=/data/kimsw.db
```

를 설정합니다.

Start Command가 필요하면:

```bash
python main.py
```

를 사용하면 됩니다.

### SQLite 주의

Railway의 일반 파일 시스템은 서비스 재배포/환경 변화에 따라 데이터가 영구 보존되지 않을 수 있습니다.

학습 데이터를 계속 보존하려면 Railway의 **Volume**을 연결하고 `/data`를 마운트 포인트로 사용하세요.

그 경우:

```env
DATABASE_PATH=/data/kimsw.db
```

로 설정하면 됩니다.

## GitHub에 올릴 때

`.env`는 절대로 GitHub에 올리지 마세요.

`.gitignore`에 `.env`와 SQLite DB가 포함되어 있습니다.

Discord Bot Token이 GitHub에 공개되었다면 즉시 Discord Developer Portal에서 토큰을 재생성해야 합니다.
