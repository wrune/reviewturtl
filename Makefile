.PHONY: local
local:
	@uvicorn reviewturtl.api.api:app --proxy-headers --host 127.0.0.1 --port 7001 --log-level debug --reload --timeout-keep-alive 65
