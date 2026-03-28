PROJECT_NAME := $(shell basename `pwd`)
PY_SRC := src/$(subst -,_,$(PROJECT_NAME))
POETRY := poetry

include makefiles/*.mk
