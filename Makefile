.PHONY: lint install-pre-commit uninstall-pre-commit

lint:
	flake8 .

install-pre-commit:
	pre-commit install

uninstall-pre-commit:
	pre-commit uninstall

reinstall-pre-commit: uninstall-pre-commit install-pre-commit
