# 准备工作
## 准备ollama
请为你的设备安装ollama。

## 准备模型
### 使用ollama模型
你可以使用ollama中的模型，修改`chatbot.py`中的model变量，替换为你想要使用的模型。

### 使用自定义模型
你可以使用你自己微调或训练的模型，将.gguf文件和Modelfile链接或复制到`ai`文件夹下，运行setup.sh会自动安装

你也可以使用ollama命令自行安装

## 运行程序
为了运行程序，你需要安装`ollama`第三方库，可以使用`pip`安装

你需要准备一个存档，然后运行`python main.py test.sav`，会自动加载sav存档并运行。
