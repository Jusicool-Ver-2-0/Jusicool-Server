class SseFormatter:
    @staticmethod
    def to_sse(data):
        return f"data: {data}\n\n"