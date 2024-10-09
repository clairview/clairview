

.PHONY: freeze
freeze: ## compile pip packages
	@pip3 install --force-reinstall pip==22.0.4
	@pip3 install pip-tools --force-reinstall
	@python3 -m piptools compile requirements.in --output-file=requirements.txt
	@python3 -m piptools compile requirements-dev.in --output-file=requirements-dev.txt
