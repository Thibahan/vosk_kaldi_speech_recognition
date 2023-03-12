model_name = vosk-model-small-de-0.15

get_model:
ifeq ("$(wildcard $(model_name).zip)", "")
ifeq ("$(wildcard $(model_name)/*)", "")
	wget https://alphacephei.com/vosk/models/$(model_name).zip
endif
endif

ifeq ("$(wildcard $(model_name)/*)", "")
ifneq ("$(wildcard $(model_name).zip)", "")
	unzip $(model_name).zip
	rm $(model_name).zip
endif
endif
