from googletrans import Translator

translator = Translator()


def get_translator_zh_CN(text = "Hello, how are you?"):
    # 英文翻译成中文
    # text = "Hello, how are you?"
    text = text.strip()
    final_text = None
    if len(text) > 0:
        result = translator.translate(text, src='en', dest='zh-CN')
        final_text = result.text
    # print(result.text)  # 输出：你好，你好吗？

    return final_text

if __name__ == "__main__":
    text = get_timestamp()