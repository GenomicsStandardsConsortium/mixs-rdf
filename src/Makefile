# Python dataclasses
#schema/%.py: schema/%.yaml
schema/mixs.py: schema/mixs.yaml 
	gen-py-classes $< > $@.tmp && python $@.tmp && mv $@.tmp $@

