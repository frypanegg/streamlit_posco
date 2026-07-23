# Streamlit OpenAI Chatbot

OpenAI API와 Streamlit으로 만든 간단한 챗봇 페이지입니다.

## 로컬 실행

```powershell
pip install -r requirements.txt
$env:OPENAI_API_KEY="sk-..."
streamlit run app.py
```

## Streamlit Community Cloud 설정

앱 배포 후 **Settings > Secrets**에 아래 값을 등록하세요.

```toml
OPENAI_API_KEY = "sk-..."
```

사용 모델은 `app.py`의 `MODEL = "gpt-4o-mini"`로 고정되어 있습니다.
