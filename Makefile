ifndef PLATFORM
	$(error The PLATFORM variable is missing.)
endif

build:
	@echo "info Make: Building '$(PLATFORM)'"
	docker image build -t speech2text:$(PLATFORM) ./$(PLATFORM)
	@make -s run

run:
	@echo "info Make: Running '$(PLATFORM)'"
	docker run speech2text:$(PLATFORM)